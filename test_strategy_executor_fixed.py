from strategy_executor import StrategyExecutor, MockBrokerAPI, RiskManager
import time

def test_strategy_executor_with_smaller_positions():
    """Test the strategy executor with smaller position sizes."""
    print("Testing Strategy Executor with Smaller Positions...")
    
    # Initialize executor with mock broker
    executor = StrategyExecutor(initial_capital=10000.0)
    
    # Test 1: Add and activate strategies
    print("\n1. Testing Strategy Management:")
    
    strategy_config = {
        "name": "RSI_Strategy",
        "description": "Buy when RSI < 30, sell when RSI > 70",
        "parameters": {
            "rsi_buy_threshold": 30,
            "rsi_sell_threshold": 70,
            "position_size_pct": 0.02
        }
    }
    
    executor.add_strategy("RSI_Strategy", strategy_config)
    executor.activate_strategy("RSI_Strategy")
    
    print(f"Active strategies: {executor.active_strategies}")
    
    # Test 2: Execute buy signal with smaller quantity
    print("\n2. Testing Buy Signal Execution (Small Position):")
    
    buy_signal = {
        "symbol": "AAPL",
        "action": "buy",
        "quantity": 1,  # Reduced from 10 to 1
        "price": 150.0,
        "order_type": "market",
        "strategy": "RSI_Strategy"
    }
    
    result = executor.execute_signal(buy_signal)
    print(f"Buy signal result: {result}")
    
    # Test 3: Check portfolio after buy
    print("\n3. Portfolio After Buy:")
    portfolio = executor.get_portfolio_summary()
    print(f"Account info: {portfolio['account_info']}")
    print(f"Positions: {portfolio['positions']}")
    
    # Test 4: Execute another buy signal
    print("\n4. Testing Another Buy Signal:")
    
    buy_signal2 = {
        "symbol": "GOOGL",
        "action": "buy",
        "quantity": 1,  # Small position
        "price": 100.0,  # Lower price to stay within limits
        "order_type": "market",
        "strategy": "RSI_Strategy"
    }
    
    result = executor.execute_signal(buy_signal2)
    print(f"Second buy signal result: {result}")
    
    # Test 5: Execute sell signal
    print("\n5. Testing Sell Signal Execution:")
    
    sell_signal = {
        "symbol": "AAPL",
        "action": "sell",
        "quantity": 1,  # Sell the position we bought
        "price": 155.0,
        "order_type": "market",
        "strategy": "RSI_Strategy"
    }
    
    result = executor.execute_signal(sell_signal)
    print(f"Sell signal result: {result}")
    
    # Test 6: Check final portfolio
    print("\n6. Final Portfolio:")
    portfolio = executor.get_portfolio_summary()
    print(f"Final positions: {portfolio['positions']}")
    
    # Test 7: Performance metrics
    print("\n7. Performance Metrics:")
    metrics = executor.get_performance_metrics()
    print(f"Performance: {metrics}")

def test_risk_limits():
    """Test that risk limits are working correctly."""
    print("\n" + "="*50)
    print("Testing Risk Limits...")
    
    executor = StrategyExecutor(initial_capital=10000.0)
    
    # Test with position that should be allowed (1% of capital)
    print("\n1. Testing Allowed Position (1% of capital):")
    signal = {
        "symbol": "AAPL",
        "action": "buy",
        "quantity": 1,
        "price": 100.0,  # $100 position = 1% of $10,000
        "order_type": "market",
        "strategy": "test"
    }
    
    result = executor.execute_signal(signal)
    print(f"Small position result: {result['success']}")
    
    # Test with position that should be rejected (10% of capital)
    print("\n2. Testing Rejected Position (10% of capital):")
    signal = {
        "symbol": "TSLA",
        "action": "buy",
        "quantity": 10,
        "price": 100.0,  # $1000 position = 10% of $10,000 (exceeds 2% limit)
        "order_type": "market",
        "strategy": "test"
    }
    
    result = executor.execute_signal(signal)
    print(f"Large position result: {result['success']}")
    if not result['success']:
        print(f"Rejection reason: {result['reason']}")

def test_portfolio_management():
    """Test portfolio management features."""
    print("\n" + "="*50)
    print("Testing Portfolio Management...")
    
    executor = StrategyExecutor(initial_capital=10000.0)
    
    # Build a small portfolio
    signals = [
        {"symbol": "AAPL", "action": "buy", "quantity": 1, "price": 100.0, "strategy": "test1"},
        {"symbol": "GOOGL", "action": "buy", "quantity": 1, "price": 150.0, "strategy": "test2"},
    ]
    
    print("\n1. Building Portfolio:")
    for signal in signals:
        result = executor.execute_signal(signal)
        print(f"Executed {signal['symbol']}: {result['success']}")
    
    # Check portfolio
    print("\n2. Portfolio Summary:")
    portfolio = executor.get_portfolio_summary()
    print(f"Total positions: {portfolio['total_positions']}")
    print(f"Position details: {portfolio['positions']}")
    
    # Test stop-loss
    print("\n3. Setting Stop-Loss:")
    if portfolio['positions']:
        symbol = portfolio['positions'][0]['symbol']
        stop_result = executor.set_stop_loss(symbol, 90.0)
        print(f"Stop-loss for {symbol}: {stop_result}")
    
    # Test take-profit
    print("\n4. Setting Take-Profit:")
    if portfolio['positions']:
        symbol = portfolio['positions'][0]['symbol']
        tp_result = executor.set_take_profit(symbol, 120.0)
        print(f"Take-profit for {symbol}: {tp_result}")
    
    # Test closing position
    print("\n5. Closing Position:")
    if portfolio['positions']:
        symbol = portfolio['positions'][0]['symbol']
        close_result = executor.close_position(symbol)
        print(f"Close position {symbol}: {close_result}")
    
    # Final portfolio check
    print("\n6. Final Portfolio:")
    final_portfolio = executor.get_portfolio_summary()
    print(f"Final positions: {final_portfolio['total_positions']}")

if __name__ == "__main__":
    test_strategy_executor_with_smaller_positions()
    test_risk_limits()
    test_portfolio_management()
    
    print("\n" + "="*50)
    print("Fixed strategy executor testing completed!")

