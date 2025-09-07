import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import logging

# Mock implementations for broker APIs (replace with real implementations)
class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class Position:
    def __init__(self, symbol: str, quantity: float, entry_price: float, 
                 side: str, timestamp: datetime = None):
        self.symbol = symbol
        self.quantity = quantity
        self.entry_price = entry_price
        self.side = side  # 'long' or 'short'
        self.timestamp = timestamp or datetime.now()
        self.current_price = entry_price
        self.unrealized_pnl = 0.0
        self.realized_pnl = 0.0

    def update_price(self, current_price: float):
        """Update current price and calculate unrealized P&L."""
        self.current_price = current_price
        if self.side == 'long':
            self.unrealized_pnl = (current_price - self.entry_price) * self.quantity
        else:  # short
            self.unrealized_pnl = (self.entry_price - current_price) * self.quantity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "current_price": self.current_price,
            "side": self.side,
            "timestamp": self.timestamp.isoformat(),
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl
        }

class Order:
    def __init__(self, symbol: str, side: OrderSide, order_type: OrderType, 
                 quantity: float, price: float = None):
        self.id = f"order_{int(time.time() * 1000)}"
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.status = OrderStatus.PENDING
        self.filled_quantity = 0.0
        self.filled_price = 0.0
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "symbol": self.symbol,
            "side": self.side.value,
            "type": self.order_type.value,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status.value,
            "filled_quantity": self.filled_quantity,
            "filled_price": self.filled_price,
            "timestamp": self.timestamp.isoformat()
        }

class RiskManager:
    def __init__(self, max_position_size_pct: float = 0.02, 
                 max_daily_loss_pct: float = 0.05,
                 max_total_exposure_pct: float = 0.20):
        """
        Initialize risk manager.
        
        Args:
            max_position_size_pct: Maximum position size as % of total capital
            max_daily_loss_pct: Maximum daily loss as % of total capital
            max_total_exposure_pct: Maximum total exposure as % of total capital
        """
        self.max_position_size_pct = max_position_size_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_total_exposure_pct = max_total_exposure_pct
        self.daily_pnl = 0.0
        self.daily_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def check_position_size(self, symbol: str, quantity: float, price: float, 
                          total_capital: float) -> Dict[str, Any]:
        """Check if position size is within risk limits."""
        position_value = quantity * price
        position_size_pct = position_value / total_capital
        
        if position_size_pct > self.max_position_size_pct:
            return {
                "allowed": False,
                "reason": f"Position size {position_size_pct:.2%} exceeds limit {self.max_position_size_pct:.2%}",
                "max_quantity": int((total_capital * self.max_position_size_pct) / price)
            }
        
        return {"allowed": True, "position_size_pct": position_size_pct}

    def check_daily_loss_limit(self, total_capital: float) -> Dict[str, Any]:
        """Check if daily loss limit is exceeded."""
        # Reset daily P&L if it's a new day
        current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if current_day > self.daily_reset_time:
            self.daily_pnl = 0.0
            self.daily_reset_time = current_day
        
        daily_loss_pct = abs(self.daily_pnl) / total_capital if self.daily_pnl < 0 else 0
        
        if daily_loss_pct > self.max_daily_loss_pct:
            return {
                "allowed": False,
                "reason": f"Daily loss {daily_loss_pct:.2%} exceeds limit {self.max_daily_loss_pct:.2%}",
                "daily_pnl": self.daily_pnl
            }
        
        return {"allowed": True, "daily_loss_pct": daily_loss_pct}

    def update_daily_pnl(self, pnl: float):
        """Update daily P&L."""
        self.daily_pnl += pnl

class MockBrokerAPI:
    """Mock broker API for testing purposes."""
    
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.positions = {}
        self.orders = {}
        self.order_history = []
        
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        total_equity = self.balance
        for position in self.positions.values():
            total_equity += position.unrealized_pnl
        
        return {
            "balance": self.balance,
            "equity": total_equity,
            "buying_power": self.balance,
            "positions_count": len(self.positions)
        }
    
    def place_order(self, order: Order) -> Dict[str, Any]:
        """Place an order (mock implementation)."""
        # Simulate order execution
        self.orders[order.id] = order
        
        # For market orders, simulate immediate execution
        if order.order_type == OrderType.MARKET:
            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            order.filled_price = order.price or 100.0  # Mock price
            
            # Update positions
            self._update_position_from_order(order)
        
        self.order_history.append(order)
        return {"order_id": order.id, "status": order.status.value}
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order."""
        if order_id in self.orders:
            self.orders[order_id].status = OrderStatus.CANCELLED
            return {"order_id": order_id, "status": "cancelled"}
        return {"error": "Order not found"}
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all positions."""
        return [pos.to_dict() for pos in self.positions.values()]
    
    def _update_position_from_order(self, order: Order):
        """Update positions based on filled order."""
        symbol = order.symbol
        
        if symbol not in self.positions:
            if order.side == OrderSide.BUY:
                self.positions[symbol] = Position(
                    symbol, order.filled_quantity, order.filled_price, 'long'
                )
            else:
                self.positions[symbol] = Position(
                    symbol, order.filled_quantity, order.filled_price, 'short'
                )
        else:
            # Update existing position
            position = self.positions[symbol]
            if order.side == OrderSide.BUY:
                if position.side == 'long':
                    # Add to long position
                    new_quantity = position.quantity + order.filled_quantity
                    new_avg_price = ((position.quantity * position.entry_price) + 
                                   (order.filled_quantity * order.filled_price)) / new_quantity
                    position.quantity = new_quantity
                    position.entry_price = new_avg_price
                else:
                    # Reduce short position
                    position.quantity -= order.filled_quantity
                    if position.quantity <= 0:
                        del self.positions[symbol]
            else:  # SELL
                if position.side == 'long':
                    # Reduce long position
                    position.quantity -= order.filled_quantity
                    if position.quantity <= 0:
                        del self.positions[symbol]
                else:
                    # Add to short position
                    new_quantity = position.quantity + order.filled_quantity
                    new_avg_price = ((position.quantity * position.entry_price) + 
                                   (order.filled_quantity * order.filled_price)) / new_quantity
                    position.quantity = new_quantity
                    position.entry_price = new_avg_price

class StrategyExecutor:
    def __init__(self, broker_api=None, initial_capital: float = 10000.0):
        """
        Initialize strategy executor.
        
        Args:
            broker_api: Broker API instance (uses mock if None)
            initial_capital: Initial capital amount
        """
        self.broker = broker_api or MockBrokerAPI(initial_capital)
        self.risk_manager = RiskManager()
        self.strategies = {}
        self.active_strategies = set()
        self.total_capital = initial_capital
        
        # Strategy execution history
        self.execution_history = []
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def add_strategy(self, strategy_name: str, strategy_config: Dict[str, Any]):
        """Add a trading strategy."""
        self.strategies[strategy_name] = strategy_config
        self.logger.info(f"Added strategy: {strategy_name}")

    def activate_strategy(self, strategy_name: str):
        """Activate a strategy for execution."""
        if strategy_name in self.strategies:
            self.active_strategies.add(strategy_name)
            self.logger.info(f"Activated strategy: {strategy_name}")
        else:
            self.logger.error(f"Strategy not found: {strategy_name}")

    def deactivate_strategy(self, strategy_name: str):
        """Deactivate a strategy."""
        self.active_strategies.discard(strategy_name)
        self.logger.info(f"Deactivated strategy: {strategy_name}")

    def execute_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a trading signal.
        
        Args:
            signal: Trading signal dictionary with keys:
                   - symbol: Asset symbol
                   - action: 'buy' or 'sell'
                   - quantity: Number of shares/units
                   - price: Target price (optional for market orders)
                   - order_type: 'market', 'limit', etc.
                   - strategy: Strategy name that generated the signal
        
        Returns:
            Execution result dictionary
        """
        try:
            symbol = signal['symbol']
            action = signal['action'].lower()
            quantity = signal['quantity']
            price = signal.get('price')
            order_type = signal.get('order_type', 'market')
            strategy = signal.get('strategy', 'unknown')
            
            # Risk checks
            risk_check = self._perform_risk_checks(symbol, quantity, price or 100.0)
            if not risk_check['allowed']:
                return {
                    "success": False,
                    "reason": risk_check['reason'],
                    "signal": signal
                }
            
            # Create order
            side = OrderSide.BUY if action == 'buy' else OrderSide.SELL
            order_type_enum = OrderType.MARKET if order_type == 'market' else OrderType.LIMIT
            
            order = Order(symbol, side, order_type_enum, quantity, price)
            
            # Execute order
            result = self.broker.place_order(order)
            
            # Log execution
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "signal": signal,
                "order": order.to_dict(),
                "result": result,
                "strategy": strategy
            }
            self.execution_history.append(execution_record)
            
            self.logger.info(f"Executed signal: {signal} -> {result}")
            
            return {
                "success": True,
                "order_id": result.get('order_id'),
                "execution_record": execution_record
            }
            
        except Exception as e:
            self.logger.error(f"Error executing signal: {e}")
            return {
                "success": False,
                "error": str(e),
                "signal": signal
            }

    def _perform_risk_checks(self, symbol: str, quantity: float, price: float) -> Dict[str, Any]:
        """Perform comprehensive risk checks."""
        # Check position size
        position_check = self.risk_manager.check_position_size(
            symbol, quantity, price, self.total_capital
        )
        if not position_check['allowed']:
            return position_check
        
        # Check daily loss limit
        daily_loss_check = self.risk_manager.check_daily_loss_limit(self.total_capital)
        if not daily_loss_check['allowed']:
            return daily_loss_check
        
        # Check account balance
        account_info = self.broker.get_account_info()
        required_capital = quantity * price
        if required_capital > account_info['buying_power']:
            return {
                "allowed": False,
                "reason": f"Insufficient buying power: {account_info['buying_power']} < {required_capital}"
            }
        
        return {"allowed": True}

    def set_stop_loss(self, symbol: str, stop_price: float) -> Dict[str, Any]:
        """Set stop-loss order for a position."""
        positions = self.broker.get_positions()
        position = next((p for p in positions if p['symbol'] == symbol), None)
        
        if not position:
            return {"success": False, "reason": "Position not found"}
        
        # Create stop-loss order
        side = OrderSide.SELL if position['side'] == 'long' else OrderSide.BUY
        order = Order(symbol, side, OrderType.STOP_LOSS, position['quantity'], stop_price)
        
        result = self.broker.place_order(order)
        return {"success": True, "order_id": result.get('order_id')}

    def set_take_profit(self, symbol: str, target_price: float) -> Dict[str, Any]:
        """Set take-profit order for a position."""
        positions = self.broker.get_positions()
        position = next((p for p in positions if p['symbol'] == symbol), None)
        
        if not position:
            return {"success": False, "reason": "Position not found"}
        
        # Create take-profit order
        side = OrderSide.SELL if position['side'] == 'long' else OrderSide.BUY
        order = Order(symbol, side, OrderType.TAKE_PROFIT, position['quantity'], target_price)
        
        result = self.broker.place_order(order)
        return {"success": True, "order_id": result.get('order_id')}

    def close_position(self, symbol: str) -> Dict[str, Any]:
        """Close a position completely."""
        positions = self.broker.get_positions()
        position = next((p for p in positions if p['symbol'] == symbol), None)
        
        if not position:
            return {"success": False, "reason": "Position not found"}
        
        # Create market order to close position
        side = OrderSide.SELL if position['side'] == 'long' else OrderSide.BUY
        order = Order(symbol, side, OrderType.MARKET, position['quantity'])
        
        result = self.broker.place_order(order)
        return {"success": True, "order_id": result.get('order_id')}

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary."""
        account_info = self.broker.get_account_info()
        positions = self.broker.get_positions()
        
        total_unrealized_pnl = sum(p['unrealized_pnl'] for p in positions)
        total_position_value = sum(p['quantity'] * p['current_price'] for p in positions)
        
        return {
            "account_info": account_info,
            "positions": positions,
            "total_positions": len(positions),
            "total_unrealized_pnl": total_unrealized_pnl,
            "total_position_value": total_position_value,
            "execution_history_count": len(self.execution_history),
            "active_strategies": list(self.active_strategies)
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics."""
        if not self.execution_history:
            return {"message": "No execution history available"}
        
        # Calculate basic metrics
        total_trades = len(self.execution_history)
        successful_trades = sum(1 for trade in self.execution_history if trade['result'].get('status') == 'filled')
        success_rate = successful_trades / total_trades if total_trades > 0 else 0
        
        # Strategy breakdown
        strategy_counts = {}
        for trade in self.execution_history:
            strategy = trade.get('strategy', 'unknown')
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1
        
        return {
            "total_trades": total_trades,
            "successful_trades": successful_trades,
            "success_rate": success_rate,
            "strategy_breakdown": strategy_counts,
            "daily_pnl": self.risk_manager.daily_pnl
        }

