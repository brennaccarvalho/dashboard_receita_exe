from db import run_query


PRODUCT_PRICE_SQL = """
product_prices AS (
    SELECT 'Produto A'::varchar AS produto, 89.99::numeric(18,2) AS preco UNION ALL
    SELECT 'Produto B', 39.95 UNION ALL
    SELECT 'Produto C', 330.00 UNION ALL
    SELECT 'Produto D', 69.29 UNION ALL
    SELECT 'Produto E', 69.87 UNION ALL
    SELECT 'Produto F', 39.95 UNION ALL
    SELECT 'Produto G', 59.93 UNION ALL
    SELECT 'Produto H', 69.29
)
"""


def get_revenue_weekly(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '7 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    revenue_current AS (
        -- TODO: ajustar schema / tabela de pedidos faturados
        SELECT
            date_trunc('week', paid_at)::date AS week_start,
            SUM(net_revenue) AS receita_total,
            COUNT(DISTINCT order_id) AS transacoes,
            SUM(CASE WHEN revenue_type = 'pontual' THEN net_revenue ELSE 0 END) AS receita_pontual,
            SUM(CASE WHEN revenue_type = 'assinatura' THEN net_revenue ELSE 0 END) AS receita_assinatura
        FROM analytics.fact_orders
        WHERE date_trunc('week', paid_at)::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1
    ),
    revenue_yoy AS (
        -- TODO: ajustar schema / comparativo com ano anterior
        SELECT
            (date_trunc('week', paid_at) + interval '1 year')::date AS week_start,
            SUM(net_revenue) AS receita_total_yoy
        FROM analytics.fact_orders
        WHERE date_trunc('week', paid_at)::date BETWEEN
            ((SELECT MIN(week_start) FROM weeks) - interval '1 year') AND
            ((SELECT MAX(week_start) FROM weeks) - interval '1 year')
        GROUP BY 1
    )
    SELECT
        w.week_start,
        COALESCE(rc.receita_total, 0)::numeric(18,2) AS receita_total,
        COALESCE(rc.transacoes, 0) AS transacoes,
        COALESCE(
            rc.receita_total / NULLIF(rc.transacoes, 0),
            0
        )::numeric(18,2) AS ticket_medio,
        COALESCE(rc.receita_pontual, 0)::numeric(18,2) AS receita_pontual,
        COALESCE(rc.receita_assinatura, 0)::numeric(18,2) AS receita_assinatura,
        COALESCE(ry.receita_total_yoy, 0)::numeric(18,2) AS receita_total_yoy
    FROM weeks w
    LEFT JOIN revenue_current rc USING (week_start)
    LEFT JOIN revenue_yoy ry USING (week_start)
    ORDER BY w.week_start
    """
    return run_query(sql, (week_start,))


def get_arr_subscriptions(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '7 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    arr_by_week AS (
        -- TODO: ajustar schema / fatos de assinaturas
        SELECT
            date_trunc('week', reference_date)::date AS week_start,
            SUM(arr_value) AS arr_total,
            SUM(new_arr_value) AS nova_arr_semana,
            AVG(renewal_rate_week) AS taxa_renovacao_semana
        FROM analytics.fact_subscription_kpis
        WHERE date_trunc('week', reference_date)::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1
    ),
    renew_12m AS (
        -- TODO: ajustar schema / taxa acumulada de renovacao 12m
        SELECT
            AVG(renewal_success_rate) AS taxa_renovacao_12m
        FROM analytics.fact_subscription_renewals
        WHERE renewed_at::date >= (SELECT ref_week_start FROM params) - interval '12 months'
          AND renewed_at::date <  (SELECT ref_week_start FROM params) + interval '1 week'
    ),
    expiring AS (
        -- TODO: ajustar schema / assinaturas a vencer
        SELECT
            COUNT(*) FILTER (
                WHERE expires_at::date >= (SELECT ref_week_start FROM params)
                  AND expires_at::date <  (SELECT ref_week_start FROM params) + interval '30 days'
            ) AS assinaturas_vencendo_30_dias,
            COUNT(*) FILTER (
                WHERE expires_at::date >= (SELECT ref_week_start FROM params)
                  AND expires_at::date <  (SELECT ref_week_start FROM params) + interval '60 days'
            ) AS assinaturas_vencendo_60_dias,
            COUNT(*) FILTER (
                WHERE expires_at::date >= (SELECT ref_week_start FROM params)
                  AND expires_at::date <  (SELECT ref_week_start FROM params) + interval '90 days'
            ) AS assinaturas_vencendo_90_dias
        FROM analytics.dim_subscriptions
        WHERE status = 'active'
    )
    SELECT
        w.week_start,
        COALESCE(a.arr_total, 0)::numeric(18,2) AS arr_total,
        COALESCE(a.nova_arr_semana, 0)::numeric(18,2) AS nova_arr_semana,
        COALESCE(a.taxa_renovacao_semana, 0)::numeric(18,4) AS taxa_renovacao_semana,
        COALESCE(r.taxa_renovacao_12m, 0)::numeric(18,4) AS taxa_renovacao_12m,
        COALESCE(e.assinaturas_vencendo_30_dias, 0) AS assinaturas_vencendo_30_dias,
        COALESCE(e.assinaturas_vencendo_60_dias, 0) AS assinaturas_vencendo_60_dias,
        COALESCE(e.assinaturas_vencendo_90_dias, 0) AS assinaturas_vencendo_90_dias
    FROM weeks w
    LEFT JOIN arr_by_week a USING (week_start)
    CROSS JOIN renew_12m r
    CROSS JOIN expiring e
    ORDER BY w.week_start
    """
    return run_query(sql, (week_start,))


def get_product_performance(week_start: str):
    sql = f"""
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    {PRODUCT_PRICE_SQL},
    product_carts AS (
        -- TODO: ajustar schema / eventos de carrinho por produto
        SELECT
            product_name AS produto,
            COUNT(*) FILTER (WHERE event_name = 'cart_started') AS carrinhos_iniciados,
            COUNT(*) FILTER (WHERE event_name = 'cart_completed') AS carrinhos_concluidos
        FROM analytics.fact_checkout_events
        WHERE occurred_at::date >= (SELECT ref_week_start FROM params)
          AND occurred_at::date <  (SELECT ref_week_start FROM params) + interval '1 week'
        GROUP BY 1
    )
    SELECT
        pp.produto,
        pp.preco AS preco_produto,
        COALESCE(pc.carrinhos_iniciados, 0) AS carrinhos_iniciados,
        COALESCE(pc.carrinhos_concluidos, 0) AS carrinhos_concluidos,
        (COALESCE(pc.carrinhos_concluidos, 0) * pp.preco)::numeric(18,2) AS receita_estimada
    FROM product_prices pp
    LEFT JOIN product_carts pc USING (produto)
    ORDER BY receita_estimada DESC, produto
    """
    return run_query(sql, (week_start,))


def get_channel_revenue(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '4 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    channels AS (
        SELECT 'Orgânico'::varchar AS canal UNION ALL
        SELECT 'E-mail' UNION ALL
        SELECT 'Direto' UNION ALL
        SELECT 'Redes Sociais' UNION ALL
        SELECT 'Pago' UNION ALL
        SELECT 'Alertas'
    ),
    revenue AS (
        -- TODO: ajustar schema / receita e sessoes por canal
        SELECT
            date_trunc('week', session_date)::date AS week_start,
            channel_group AS canal,
            SUM(attributed_revenue) AS receita,
            SUM(sessions) AS sessoes
        FROM analytics.fact_channel_performance
        WHERE date_trunc('week', session_date)::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1, 2
    )
    SELECT
        w.week_start,
        c.canal,
        COALESCE(r.receita, 0)::numeric(18,2) AS receita,
        COALESCE(r.sessoes, 0) AS sessoes
    FROM weeks w
    CROSS JOIN channels c
    LEFT JOIN revenue r
      ON r.week_start = w.week_start
     AND r.canal = c.canal
    ORDER BY w.week_start, c.canal
    """
    return run_query(sql, (week_start,))


def get_gsc_data(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '7 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    gsc AS (
        -- TODO: ajustar schema / tabela consolidada do GSC
        SELECT
            date_trunc('week', report_date)::date AS week_start,
            SUM(impressions) AS impressoes,
            SUM(clicks) AS cliques,
            AVG(avg_position) AS posicao_media
        FROM analytics.fact_gsc_weekly
        WHERE date_trunc('week', report_date)::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1
    )
    SELECT
        w.week_start,
        COALESCE(g.impressoes, 0) AS impressoes,
        COALESCE(g.cliques, 0) AS cliques,
        COALESCE(g.cliques::numeric / NULLIF(g.impressoes, 0), 0)::numeric(18,4) AS ctr,
        COALESCE(g.posicao_media, 0)::numeric(18,2) AS posicao_media
    FROM weeks w
    LEFT JOIN gsc g USING (week_start)
    ORDER BY w.week_start
    """
    return run_query(sql, (week_start,))


def get_email_stats(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / campanhas de email
    SELECT
        COALESCE(SUM(emails_sent), 0) AS emails_enviados,
        COALESCE(SUM(generated_sessions), 0) AS sessoes_geradas,
        COALESCE(AVG(click_through_rate), 0)::numeric(18,4) AS ctr,
        COALESCE(SUM(attributed_revenue), 0)::numeric(18,2) AS receita_atribuida
    FROM analytics.fact_email_campaigns
    WHERE campaign_date::date >= (SELECT ref_week_start FROM params)
      AND campaign_date::date <  (SELECT ref_week_start FROM params) + interval '1 week'
    """
    return run_query(sql, (week_start,))


def get_alerts_stats(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / alertas e push notifications
    SELECT
        COALESCE(SUM(alerts_sent), 0) AS alertas_enviados,
        COALESCE(SUM(generated_sessions), 0) AS sessoes_geradas,
        COALESCE(AVG(click_through_rate), 0)::numeric(18,4) AS ctr,
        COALESCE(SUM(attributed_revenue), 0)::numeric(18,2) AS receita_atribuida
    FROM analytics.fact_alert_campaigns
    WHERE alert_date::date >= (SELECT ref_week_start FROM params)
      AND alert_date::date <  (SELECT ref_week_start FROM params) + interval '1 week'
    """
    return run_query(sql, (week_start,))


def get_audience_weekly(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '7 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    audience AS (
        -- TODO: ajustar schema / kpis semanais de audiencia
        SELECT
            date_trunc('week', session_date)::date AS week_start,
            SUM(sessions) AS sessoes,
            SUM(unique_visitors) AS visitantes_unicos,
            AVG(engagement_rate) AS taxa_engajamento,
            AVG(pageviews_per_session) AS paginas_por_sessao
        FROM analytics.fact_audience_weekly
        WHERE date_trunc('week', session_date)::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1
    ),
    audience_yoy AS (
        -- TODO: ajustar schema / base YoY
        SELECT
            (date_trunc('week', session_date) + interval '1 year')::date AS week_start,
            SUM(sessions) AS sessoes_yoy
        FROM analytics.fact_audience_weekly
        WHERE date_trunc('week', session_date)::date BETWEEN
            ((SELECT MIN(week_start) FROM weeks) - interval '1 year') AND
            ((SELECT MAX(week_start) FROM weeks) - interval '1 year')
        GROUP BY 1
    )
    SELECT
        w.week_start,
        COALESCE(a.sessoes, 0) AS sessoes,
        COALESCE(a.visitantes_unicos, 0) AS visitantes_unicos,
        COALESCE(a.taxa_engajamento, 0)::numeric(18,4) AS taxa_engajamento,
        COALESCE(a.paginas_por_sessao, 0)::numeric(18,2) AS paginas_por_sessao,
        COALESCE(y.sessoes_yoy, 0) AS sessoes_yoy
    FROM weeks w
    LEFT JOIN audience a USING (week_start)
    LEFT JOIN audience_yoy y USING (week_start)
    ORDER BY w.week_start
    """
    return run_query(sql, (week_start,))


def get_audience_profile(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / perfil de audiencia por dimensao
    SELECT
        dimension_key AS dimensao,
        segment_label AS segmento,
        SUM(sessions) AS sessoes
    FROM analytics.fact_audience_profile_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
      AND dimension_key IN ('dim1', 'dim2', 'dim3')
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    return run_query(sql, (week_start,))


def get_registration_funnel(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / funil de cadastro semanal
    SELECT
        etapa,
        contagem
    FROM analytics.fact_registration_funnel_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    ORDER BY ordem_etapa
    """
    return run_query(sql, (week_start,))


def get_registration_by_channel(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / cadastros por canal
    SELECT
        canal,
        SUM(cadastros) AS cadastros,
        AVG(score_medio) AS score_medio,
        AVG(conversao_para_venda) AS conversao_para_venda
    FROM analytics.fact_registration_channel_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    GROUP BY 1
    ORDER BY cadastros DESC, canal
    """
    return run_query(sql, (week_start,))


def get_registration_score_trend(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    ),
    weeks AS (
        SELECT generate_series(
            (SELECT ref_week_start FROM params) - interval '7 weeks',
            (SELECT ref_week_start FROM params),
            interval '1 week'
        )::date AS week_start
    ),
    scores AS (
        -- TODO: ajustar schema / score medio semanal
        SELECT
            week_start::date AS week_start,
            AVG(score_medio) AS score_medio
        FROM analytics.fact_registration_channel_weekly
        WHERE week_start::date BETWEEN
            (SELECT MIN(week_start) FROM weeks) AND (SELECT MAX(week_start) FROM weeks)
        GROUP BY 1
    )
    SELECT
        w.week_start,
        COALESCE(s.score_medio, 0)::numeric(18,2) AS score_medio
    FROM weeks w
    LEFT JOIN scores s USING (week_start)
    ORDER BY w.week_start
    """
    return run_query(sql, (week_start,))


def get_checkout_funnel_traditional(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / funil do checkout tradicional
    SELECT
        etapa,
        carrinhos,
        conversao_pct,
        abandono_pct
    FROM analytics.fact_checkout_funnel_traditional_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    ORDER BY ordem_etapa
    """
    return run_query(sql, (week_start,))


def get_checkout_funnel_quick(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / funil da compra rapida
    SELECT
        etapa,
        carrinhos,
        conversao_pct,
        abandono_pct
    FROM analytics.fact_checkout_funnel_quick_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    ORDER BY ordem_etapa
    """
    return run_query(sql, (week_start,))


def get_cart_recovery(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / recuperacao de carrinho
    SELECT
        COALESCE(SUM(elegiveis), 0) AS elegiveis,
        COALESCE(SUM(mensagens_enviadas), 0) AS mensagens_enviadas,
        COALESCE(SUM(recuperados), 0) AS recuperados,
        COALESCE(AVG(taxa_recuperacao), 0)::numeric(18,4) AS taxa_recuperacao,
        COALESCE(SUM(receita_recuperada), 0)::numeric(18,2) AS receita_recuperada
    FROM analytics.fact_cart_recovery_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    """
    return run_query(sql, (week_start,))


def get_payment_conversion(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / conversao por meio de pagamento
    SELECT
        payment_method AS meio_pagamento,
        AVG(concluidos_pct) AS concluidos_pct,
        AVG(abandono_pct) AS abandono_pct
    FROM analytics.fact_payment_conversion_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    GROUP BY 1
    ORDER BY concluidos_pct DESC, meio_pagamento
    """
    return run_query(sql, (week_start,))


def get_upsell_vitrine(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / vitrine de upsell
    SELECT
        COALESCE(AVG(taxa_adicao), 0)::numeric(18,4) AS taxa_adicao,
        COALESCE(AVG(impacto_ticket_medio), 0)::numeric(18,2) AS impacto_ticket_medio,
        COALESCE(SUM(carrinhos_com_upsell), 0) AS carrinhos_com_upsell,
        COALESCE(SUM(receita_incremental), 0)::numeric(18,2) AS receita_incremental
    FROM analytics.fact_checkout_upsell_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
    """
    return run_query(sql, (week_start,))


def get_conversion_by_segment(week_start: str):
    sql = """
    WITH params AS (
        SELECT %s::date AS ref_week_start
    )
    -- TODO: ajustar schema / conversao por segmentacao
    SELECT
        segmentacao,
        segmento,
        AVG(conversao_pct) AS conversao_pct
    FROM analytics.fact_checkout_conversion_segment_weekly
    WHERE week_start::date = (SELECT ref_week_start FROM params)
      AND segmentacao IN ('perfil_comercial', 'perfil_engajamento', 'safra_cadastro')
    GROUP BY 1, 2
    ORDER BY 1, 3 DESC, 2
    """
    return run_query(sql, (week_start,))
