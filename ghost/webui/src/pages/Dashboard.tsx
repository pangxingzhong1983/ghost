import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Typography, Space, Spin, Alert } from 'antd';
import {
  UsergroupAddOutlined,
  GlobalOutlined,
  KeyOutlined,
  OrderedListOutlined,
  ClockCircleOutlined,
  AppstoreAddOutlined,
} from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import websocketService from '../services/websocket';

const { Title } = Typography;

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    sessions: 0,
    listeners: 0,
    credentials: 12,
    jobs: 2,
    payloads: 8,
  });

  // 会话趋势数据
  const [sessionData, setSessionData] = useState([
    { name: '10:00', count: 1 },
    { name: '11:00', count: 2 },
    { name: '12:00', count: 3 },
    { name: '13:00', count: 2 },
    { name: '14:00', count: 4 },
    { name: '15:00', count: 5 },
    { name: '16:00', count: 5 },
  ]);

  // 平台分布数据
  const [platformData, setPlatformData] = useState([
    { name: 'Windows', value: 3 },
    { name: 'Linux', value: 1 },
    { name: 'macOS', value: 1 },
  ]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 检查WebSocket连接状态
        if (!websocketService.isConnected()) {
          await websocketService.connect();
        }

        // 获取会话数据
        const sessions = await websocketService.getSessions();
        setStats(prev => ({
          ...prev,
          sessions: sessions.length,
        }));

        // 分析平台分布
        const platformCount: { [key: string]: number } = {
          Windows: 0,
          Linux: 0,
          macOS: 0,
          Android: 0
        };

        sessions.forEach((session: any) => {
          if (session.platform) {
            if (session.platform.includes('Windows')) {
              platformCount.Windows++;
            } else if (session.platform.includes('Linux')) {
              platformCount.Linux++;
            } else if (session.platform.includes('macOS') || session.platform.includes('Darwin')) {
              platformCount.macOS++;
            } else if (session.platform.includes('Android')) {
              platformCount.Android++;
            }
          }
        });

        setPlatformData(Object.entries(platformCount).map(([name, value]) => ({ name, value })));

        // 获取监听器数据
        const listeners = await websocketService.getListeners();
        setStats(prev => ({
          ...prev,
          listeners: listeners.length,
        }));

        // 获取凭证数据
        const credentials = await websocketService.getCredentials();
        setStats(prev => ({
          ...prev,
          credentials: credentials.length,
        }));

        // 获取作业数据
        const jobs = await websocketService.getJobs();
        setStats(prev => ({
          ...prev,
          jobs: jobs.length,
        }));

        // 模拟会话趋势数据
        const hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'];
        const trendData = hours.map(hour => ({
          name: hour,
          count: Math.floor(Math.random() * 5) + 1
        }));
        setSessionData(trendData);

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // 即使WebSocket连接失败，也显示模拟数据
        setStats(prev => ({
          ...prev,
          sessions: 5,
          listeners: 3,
        }));
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // 每30秒刷新一次数据
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <Title level={2}>仪表盘</Title>
      
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          <Row gutter={16}>
            <Col span={6}>
              <Card>
                <Statistic
                  title="活跃会话"
                  value={stats.sessions}
                  prefix={<UsergroupAddOutlined />}
                  suffix="个"
                  valueStyle={{ color: '#3f8600' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="监听器"
                  value={stats.listeners}
                  prefix={<GlobalOutlined />}
                  suffix="个"
                  valueStyle={{ color: '#1890ff' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="凭证"
                  value={stats.credentials}
                  prefix={<KeyOutlined />}
                  suffix="个"
                  valueStyle={{ color: '#722ed1' }}
                />
              </Card>
            </Col>
            <Col span={6}>
              <Card>
                <Statistic
                  title="活跃作业"
                  value={stats.jobs}
                  prefix={<OrderedListOutlined />}
                  suffix="个"
                  valueStyle={{ color: '#eb2f96' }}
                />
              </Card>
            </Col>
          </Row>

          <Row gutter={16} style={{ marginTop: 16 }}>
            <Col span={12}>
              <Card title="会话趋势" extra={<ClockCircleOutlined />}>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={sessionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="count" stroke="#1890ff" activeDot={{ r: 8 }} />
                  </LineChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="平台分布" extra={<AppstoreAddOutlined />}>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={platformData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent = 0 }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    >
                      {platformData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Card>
            </Col>
          </Row>

          <Row style={{ marginTop: 16 }}>
            <Col span={24}>
              <Card title="最近活动">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Alert message="会话 #1 已连接 (Windows 10, 192.168.1.100)" type="success" />
                  <Alert message="监听器 tcp/443 已启动" type="info" />
                  <Alert message="Payload 已生成 (Windows x64)" type="info" />
                  <Alert message="模块 mimikatz 执行成功" type="success" />
                  <Alert message="凭证已添加 (Administrator:Password123)" type="success" />
                </Space>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
};

export default Dashboard;