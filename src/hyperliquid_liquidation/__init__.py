"""Liquidation level analysis and heatmaps for Hyperliquid perpetual markets.

Modules:
    config                  configuration constants and dataclasses
    hyperliquid_api         client for the public Hyperliquid info API
    scraper                 whale data collection from Hypurrscan
    liquidation_calculator  liquidation prices and price-level aggregation
    heatmap_visualizer      matplotlib, plotly and terminal output
    main                    LiquidationHeatmapGenerator and the CLI
"""
