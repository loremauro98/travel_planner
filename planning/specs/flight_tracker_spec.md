# Flight Tracker Spec

## Goal
Build a system that automatically scans for flights and uses statistical methods (moving averages) to identify the best time to book, factoring in historical trends and intra-day oscillations.

## Features
1. **Multi-Airport Routing**: User inputs regions (e.g., "Switzerland to Norway"). The system calculates all valid airport pairings.
2. **Moving Averages (MA)**: Calculate short-term (e.g., 3-day, 7-day) and long-term (e.g., 14-day, 30-day) MA for prices.
3. **Dip Detection**: Trigger a "Buy Now" alert when current price is significantly below the MA.
4. **Historical Grounding**: Compare current trends with historical data for the same time of year (e.g., December prices) to understand if prices will continue dropping or rebound.
5. **Intra-Day Tracking**: Find optimal time-slots for booking (morning vs evening price drops).
