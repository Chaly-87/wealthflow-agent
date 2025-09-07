import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  AlertTriangle, 
  Activity, 
  BarChart3,
  Settings,
  Bell,
  Eye,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell } from 'recharts'
import './App.css'

// Mock data for demonstration
const portfolioData = [
  { name: 'Jan', value: 10000 },
  { name: 'Feb', value: 10500 },
  { name: 'Mar', value: 9800 },
  { name: 'Apr', value: 11200 },
  { name: 'May', value: 12100 },
  { name: 'Jun', value: 11800 },
  { name: 'Jul', value: 13500 },
]

const assetAllocation = [
  { name: 'Stocks', value: 65, color: '#3b82f6' },
  { name: 'Crypto', value: 25, color: '#f59e0b' },
  { name: 'Cash', value: 10, color: '#10b981' },
]

const topOpportunities = [
  { symbol: 'AAPL', type: 'stock', score: 0.92, price: 175.50, change: 2.3, reason: 'Strong earnings momentum' },
  { symbol: 'BTC', type: 'crypto', score: 0.88, price: 45000, change: -1.2, reason: 'Technical breakout pattern' },
  { symbol: 'NVDA', type: 'stock', score: 0.85, price: 420.75, change: 4.1, reason: 'AI sector growth' },
]

const recentAlerts = [
  { id: 1, type: 'volume_anomaly', symbol: 'TSLA', message: 'Volume spike detected - 3.2x normal', urgency: 'high', time: '2 min ago' },
  { id: 2, type: 'sentiment_spike', symbol: 'ETH', message: 'Positive sentiment surge on social media', urgency: 'medium', time: '15 min ago' },
  { id: 3, type: 'price_alert', symbol: 'GOOGL', message: 'Price target reached: $2,500', urgency: 'low', time: '1 hour ago' },
]

const activeStrategies = [
  { name: 'RSI Momentum', status: 'active', performance: 12.5, trades: 23 },
  { name: 'Mean Reversion', status: 'active', performance: 8.2, trades: 15 },
  { name: 'Sentiment Analysis', status: 'paused', performance: -2.1, trades: 8 },
]

function App() {
  const [isMonitoring, setIsMonitoring] = useState(true)
  const [portfolioValue, setPortfolioValue] = useState(13500)
  const [dailyChange, setDailyChange] = useState(2.3)

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      if (isMonitoring) {
        const change = (Math.random() - 0.5) * 100
        setPortfolioValue(prev => Math.max(0, prev + change))
        setDailyChange((Math.random() - 0.5) * 5)
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [isMonitoring])

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm dark:bg-slate-900/80 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  WealthFlow Agent
                </h1>
              </div>
              <Badge variant={isMonitoring ? "default" : "secondary"} className="ml-4">
                {isMonitoring ? "Live" : "Paused"}
              </Badge>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button
                variant={isMonitoring ? "destructive" : "default"}
                size="sm"
                onClick={() => setIsMonitoring(!isMonitoring)}
                className="flex items-center space-x-2"
              >
                {isMonitoring ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                <span>{isMonitoring ? "Pause" : "Start"} Monitoring</span>
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="sm">
                <Bell className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Portfolio Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="md:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>Portfolio Value</span>
              </CardTitle>
              <CardDescription>Total portfolio performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="text-3xl font-bold">{formatCurrency(portfolioValue)}</div>
                <div className={`flex items-center space-x-1 text-sm ${dailyChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {dailyChange >= 0 ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                  <span>{formatPercentage(dailyChange)} today</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="w-5 h-5" />
                <span>Active Alerts</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{recentAlerts.length}</div>
              <div className="text-sm text-muted-foreground">
                {recentAlerts.filter(a => a.urgency === 'high').length} high priority
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Eye className="w-5 h-5" />
                <span>Monitoring</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <div className="text-sm text-muted-foreground">Assets tracked</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="opportunities">Opportunities</TabsTrigger>
            <TabsTrigger value="alerts">Alerts</TabsTrigger>
            <TabsTrigger value="strategies">Strategies</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Portfolio Chart */}
              <Card>
                <CardHeader>
                  <CardTitle>Portfolio Performance</CardTitle>
                  <CardDescription>7-month performance overview</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={portfolioData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip formatter={(value) => [formatCurrency(value), 'Portfolio Value']} />
                      <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.1} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Asset Allocation */}
              <Card>
                <CardHeader>
                  <CardTitle>Asset Allocation</CardTitle>
                  <CardDescription>Current portfolio distribution</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={assetAllocation}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {assetAllocation.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value}%`, 'Allocation']} />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="flex justify-center space-x-4 mt-4">
                    {assetAllocation.map((item, index) => (
                      <div key={index} className="flex items-center space-x-2">
                        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                        <span className="text-sm">{item.name} ({item.value}%)</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="opportunities" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <TrendingUp className="w-5 h-5" />
                  <span>Top Opportunities</span>
                </CardTitle>
                <CardDescription>AI-identified investment opportunities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topOpportunities.map((opp, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                      <div className="flex items-center space-x-4">
                        <div className="text-center">
                          <div className="font-bold">{opp.symbol}</div>
                          <Badge variant="outline" className="text-xs">
                            {opp.type}
                          </Badge>
                        </div>
                        <div>
                          <div className="font-medium">{formatCurrency(opp.price)}</div>
                          <div className={`text-sm ${opp.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {formatPercentage(opp.change)}
                          </div>
                        </div>
                        <div className="flex-1">
                          <div className="text-sm text-muted-foreground">{opp.reason}</div>
                          <div className="flex items-center space-x-2 mt-1">
                            <span className="text-xs">Score:</span>
                            <Progress value={opp.score * 100} className="w-20 h-2" />
                            <span className="text-xs font-medium">{(opp.score * 100).toFixed(0)}%</span>
                          </div>
                        </div>
                      </div>
                      <Button size="sm">View Details</Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="alerts" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <AlertTriangle className="w-5 h-5" />
                  <span>Recent Alerts</span>
                </CardTitle>
                <CardDescription>Real-time market alerts and notifications</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentAlerts.map((alert) => (
                    <Alert key={alert.id} className={`${
                      alert.urgency === 'high' ? 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950' :
                      alert.urgency === 'medium' ? 'border-yellow-200 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-950' :
                      'border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950'
                    }`}>
                      <AlertTriangle className="h-4 w-4" />
                      <AlertTitle className="flex items-center justify-between">
                        <span>{alert.symbol} - {alert.type.replace('_', ' ').toUpperCase()}</span>
                        <div className="flex items-center space-x-2">
                          <Badge variant={
                            alert.urgency === 'high' ? 'destructive' :
                            alert.urgency === 'medium' ? 'default' : 'secondary'
                          }>
                            {alert.urgency}
                          </Badge>
                          <span className="text-xs text-muted-foreground">{alert.time}</span>
                        </div>
                      </AlertTitle>
                      <AlertDescription>{alert.message}</AlertDescription>
                    </Alert>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="strategies" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Settings className="w-5 h-5" />
                  <span>Active Strategies</span>
                </CardTitle>
                <CardDescription>Automated trading strategies performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {activeStrategies.map((strategy, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div>
                          <div className="font-medium">{strategy.name}</div>
                          <div className="text-sm text-muted-foreground">{strategy.trades} trades executed</div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <div className={`font-medium ${strategy.performance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {formatPercentage(strategy.performance)}
                          </div>
                          <div className="text-sm text-muted-foreground">Performance</div>
                        </div>
                        <Badge variant={strategy.status === 'active' ? 'default' : 'secondary'}>
                          {strategy.status}
                        </Badge>
                        <Button variant="outline" size="sm">
                          {strategy.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reports" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <RefreshCw className="w-5 h-5" />
                  <span>Daily Reports</span>
                </CardTitle>
                <CardDescription>Automated market analysis and insights</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <div className="font-medium">Today's Market Report</div>
                      <div className="text-sm text-muted-foreground">Generated at 8:00 AM</div>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">View</Button>
                      <Button variant="outline" size="sm">Download</Button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <div className="font-medium">Weekly Performance Summary</div>
                      <div className="text-sm text-muted-foreground">Generated yesterday</div>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">View</Button>
                      <Button variant="outline" size="sm">Download</Button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <div className="font-medium">Monthly Strategy Review</div>
                      <div className="text-sm text-muted-foreground">Generated 3 days ago</div>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">View</Button>
                      <Button variant="outline" size="sm">Download</Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

