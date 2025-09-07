from strategy_executor import StrategyExecutor, MockBrokerAPI, RiskManager
import time

def test_strategy_executor():
    """Test the strategy executor functionality."""
    print("Testing Strategy Executor...")
    
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
    
    # Test 2: Execute buy signal
    print("\n2. Testing Buy Signal Execution:")
    
    buy_signal = {
        "symbol": "AAPL",
        "action": "buy",
        "quantity": 10,
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
    
    # Test 4: Execute sell signal
    print("\n4. Testing Sell Signal Execution:")
    
    sell_signal = {
        "symbol": "AAPL",
        "action": "sell",
        "quantity": 5,
        "price": 155.0,
        "order_type": "market",
        "strategy": "RSI_Strategy"
    }
    
    result = executor.execute_signal(sell_signal)
    print(f"Sell signal result: {result}")
    
    # Test 5: Set stop-loss and take-profit
    print("\n5. Testing Risk Management Orders:")
    
    stop_loss_result = executor.set_stop_loss("AAPL", 140.0)
    print(f"Stop-loss result: {stop_loss_result}")
    
    take_profit_result = executor.set_take_profit("AAPL", 160.0)
    print(f"Take-profit result: {take_profit_result}")
    
    # Test 6: Performance metrics
    print("\n6. Performance Metrics:")
    metrics = executor.get_performance_metrics()
    print(f"Performance: {metrics}")

def test_risk_manager():
    """Test the risk manager functionality."""
    print("\n" + "="*50)
    print("Testing Risk Manager...")
    
    risk_manager = RiskManager(
        max_position_size_pct=0.02,  # 2% max position size
        max_daily_loss_pct=0.05,    # 5% max daily loss
        max_total_exposure_pct=0.20  # 20% max total exposure
    )
    
    total_capital = 10000.0
    
    # Test 1: Position size check (within limits)
    print("\n1. Testing Position Size Check (Within Limits):")
    result = risk_manager.check_position_size("AAPL", 1, 150.0, total_capital)
    print(f"Position size check (1 share @ $150): {result}")
    
    # Test 2: Position size check (exceeds limits)
    print("\n2. Testing Position Size Check (Exceeds Limits):")
    result = risk_manager.check_position_size("AAPL", 100, 150.0, total_capital)
    print(f"Position size check (100 shares @ $150): {result}")
    
    # Test 3: Daily loss limit check
    print("\n3. Testing Daily Loss Limit:")
    result = risk_manager.check_daily_loss_limit(total_capital)
    print(f"Daily loss check (initial): {result}")
    
    # Simulate a loss
    risk_manager.update_daily_pnl(-300.0)  # $300 loss
    result = risk_manager.check_daily_loss_limit(total_capital)
    print(f"Daily loss check (after $300 loss): {result}")
    
    # Simulate a big loss
    risk_manager.update_daily_pnl(-400.0)  # Additional $400 loss (total $700)
    result = risk_manager.check_daily_loss_limit(total_capital)
    print(f"Daily loss check (after $700 total loss): {result}")

def test_mock_broker():
    """Test the mock broker API."""
    print("\n" + "="*50)
    print("Testing Mock Broker API...")
    
    broker = MockBrokerAPI(initial_balance=10000.0)
    
    # Test 1: Account info
    print("\n1. Initial Account Info:")
    account_info = broker.get_account_info()
    print(f"Account: {account_info}")
    
    # Test 2: Place buy order
    print("\n2. Placing Buy Order:")
    from strategy_executor import Order, OrderSide, OrderType
    
    buy_order = Order("AAPL", OrderSide.BUY, OrderType.MARKET, 10, 150.0)
    result = broker.place_order(buy_order)
    print(f"Buy order result: {result}")
    
    # Test 3: Check positions
    print("\n3. Positions After Buy:")
    positions = broker.get_positions()
    print(f"Positions: {positions}")
    
    # Test 4: Place sell order
    print("\n4. Placing Sell Order:")
    sell_order = Order("AAPL", OrderSide.SELL, OrderType.MARKET, 5, 155.0)
    result = broker.place_order(sell_order)
    print(f"Sell order result: {result}")
    
    # Test 5: Final positions
    print("\n5. Final Positions:")
    positions = broker.get_positions()
    print(f"Final positions: {positions}")

def test_integration():
    """Test integration between all components."""
    print("\n" + "="*50)
    print("Testing Integration...")
    
    # Create a complete trading scenario
    executor = StrategyExecutor(initial_capital=10000.0)
    
    # Add multiple strategies
    strategies = {
        "Momentum_Strategy": {
            "description": "Buy on momentum, sell on reversal",
            "parameters": {"momentum_threshold": 0.05}
        },
        "Mean_Reversion": {
            "description": "Buy oversold, sell overbought",
            "parameters": {"oversold_threshold": 30, "overbought_threshold": 70}
        }
    }
    
    for name, config in strategies.items():
        executor.add_strategy(name, config)
        executor.activate_strategy(name)
    
    # Execute multiple signals
    signals = [
        {"symbol": "AAPL", "action": "buy", "quantity": 5, "price": 150.0, "strategy": "Momentum_Strategy"},
        {"symbol": "GOOGL", "action": "buy", "quantity": 2, "price": 2500.0, "strategy": "Mean_Reversion"},
        {"symbol": "TSLA", "action": "buy", "quantity": 3, "price": 800.0, "strategy": "Momentum_Strategy"},
        {"symbol": "AAPL", "action": "sell", "quantity": 2, "price": 155.0, "strategy": "Momentum_Strategy"},
    ]
    
    print("\nExecuting multiple trading signals:")
    for i, signal in enumerate(signals, 1):
        result = executor.execute_signal(signal)
        print(f"Signal {i}: {signal['action']} {signal['quantity']} {signal['symbol']} -> {result['success']}")
        time.sleep(0.1)  # Small delay between orders
    
    # Final portfolio summary
    print("\nFinal Portfolio Summary:")
    portfolio = executor.get_portfolio_summary()
    print(f"Total positions: {portfolio['total_positions']}")
    print(f"Total unrealized P&L: ${portfolio['total_unrealized_pnl']:.2f}")
    print(f"Active strategies: {portfolio['active_strategies']}")
    
    # Performance metrics
    print("\nPerformance Metrics:")
    metrics = executor.get_performance_metrics()
    print(f"Total trades: {metrics['total_trades']}")
    print(f"Success rate: {metrics['success_rate']:.2%}")
    print(f"Strategy breakdown: {metrics['strategy_breakdown']}")

if __name__ == "__main__":
    test_strategy_executor()
    test_risk_manager()
    test_mock_broker()
    test_integration()
    
    print("\n" + "="*50)
    print("Strategy executor testing completed!")

