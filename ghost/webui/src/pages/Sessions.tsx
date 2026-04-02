import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Modal, message, Spin, Form, Input } from 'antd';
import websocketService from '../services/websocket';

const { Title } = Typography;

interface Session {
  id: string;
  name: string;
  platform: string;
  arch: string;
  ip: string;
  user: string;
  hostname: string;
  status: 'active' | 'inactive';
  last_seen: string;
  created_at: string;
  os: string;
  privileges: string;
}

const Sessions: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [selectedSession, setSelectedSession] = useState<Session | null>(null);
  const [commandModalVisible, setCommandModalVisible] = useState(false);
  const [activeSession, setActiveSession] = useState<string | null>(null);
  const [commandHistory, setCommandHistory] = useState<{id: string, command: string, output: string, timestamp: string}[]>([]);

  // 模拟数据
  const mockSessions: Session[] = [
    {
      id: '1',
      name: 'Session #1',
      platform: 'windows',
      arch: 'x64',
      ip: '192.168.1.101',
      user: 'Administrator',
      hostname: 'WIN-SERVER',
      status: 'active',
      last_seen: '2026-03-30 14:30:00',
      created_at: '2026-03-30 10:00:00',
      os: 'Windows Server 2019',
      privileges: 'SYSTEM',
    },
    {
      id: '2',
      name: 'Session #2',
      platform: 'linux',
      arch: 'x64',
      ip: '192.168.1.102',
      user: 'root',
      hostname: 'ubuntu-server',
      status: 'active',
      last_seen: '2026-03-30 14:25:00',
      created_at: '2026-03-30 10:30:00',
      os: 'Ubuntu 20.04 LTS',
      privileges: 'root',
    },
    {
      id: '3',
      name: 'Session #3',
      platform: 'macos',
      arch: 'x64',
      ip: '192.168.1.103',
      user: 'admin',
      hostname: 'macbook-pro',
      status: 'inactive',
      last_seen: '2026-03-30 14:00:00',
      created_at: '2026-03-30 09:00:00',
      os: 'macOS Big Sur',
      privileges: 'admin',
    },
  ];

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        setLoading(true);
        // 检查WebSocket连接状态
        if (!websocketService.isConnected()) {
          await websocketService.connect();
        }
        // 获取会话列表
        const sessions = await websocketService.getSessions();
        setSessions(sessions);
      } catch (error) {
        console.error('Error fetching sessions:', error);
        // 使用模拟数据作为fallback
        setSessions(mockSessions);
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();

    // 每30秒刷新一次会话列表
    const interval = setInterval(fetchSessions, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSessionDetail = (session: Session) => {
    setSelectedSession(session);
    setDetailModalVisible(true);
  };

  const handleSendCommand = (sessionId: string) => {
    setActiveSession(sessionId);
    setCommandModalVisible(true);
  };

  const handleExecuteCommand = async (values: {command: string}) => {
    try {
      setLoading(true);
      // 使用WebSocket服务执行命令
      const output = await websocketService.executeCommand('session', [activeSession!, 'run', values.command]);
      const newCommand = {
        id: (commandHistory.length + 1).toString(),
        command: values.command,
        output: `Command executed: ${values.command}\nOutput: ${output}`,
        timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '),
      };
      setCommandHistory([...commandHistory, newCommand]);
      message.success('命令执行成功');
    } catch (error) {
      console.error('Error executing command:', error);
      message.error('命令执行失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSession = async (id: string) => {
    try {
      // 使用WebSocket服务关闭会话
      await websocketService.executeCommand('session', [id, 'close']);
      setSessions(sessions.map(session => 
        session.id === id ? { ...session, status: 'inactive' } : session
      ));
      message.success('会话已关闭');
    } catch (error) {
      console.error('Error closing session:', error);
      message.error('会话关闭失败');
    }
  };

  const columns = [
    {
      title: '会话',
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <span>{name}</span>,
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
      filters: [
        { text: 'Windows', value: 'windows' },
        { text: 'Linux', value: 'linux' },
        { text: 'macOS', value: 'macos' },
      ],
      onFilter: (value: any, record: Session) => record.platform === value,
      render: (platform: string) => (
        <Tag color={platform === 'windows' ? 'blue' : platform === 'linux' ? 'green' : 'purple'}>
          {platform}
        </Tag>
      ),
    },
    {
      title: '用户',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: 'IP地址',
      dataIndex: 'ip',
      key: 'ip',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '活动' : '非活动'}
        </Tag>
      ),
    },
    {
      title: '最后活跃',
      dataIndex: 'last_seen',
      key: 'last_seen',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Session) => (
        <Space size="middle">
          <Button type="primary" size="small" onClick={() => handleSendCommand(record.id)}>
            执行命令
          </Button>
          <Button size="small" onClick={() => handleSessionDetail(record)}>
            详情
          </Button>
          <Button danger size="small" onClick={() => handleCloseSession(record.id)}>
            关闭
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>会话管理</Title>
      
      <Card>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={sessions} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title="会话详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>,
        ]}
        width={600}
      >
        {selectedSession && (
          <div>
            <p><strong>会话:</strong> {selectedSession.name}</p>
            <p><strong>平台:</strong> {selectedSession.platform}</p>
            <p><strong>架构:</strong> {selectedSession.arch}</p>
            <p><strong>IP地址:</strong> {selectedSession.ip}</p>
            <p><strong>用户:</strong> {selectedSession.user}</p>
            <p><strong>主机名:</strong> {selectedSession.hostname}</p>
            <p><strong>状态:</strong> {selectedSession.status}</p>
            <p><strong>操作系统:</strong> {selectedSession.os}</p>
            <p><strong>权限:</strong> {selectedSession.privileges}</p>
            <p><strong>创建时间:</strong> {selectedSession.created_at}</p>
            <p><strong>最后活跃:</strong> {selectedSession.last_seen}</p>
          </div>
        )}
      </Modal>

      <Modal
        title={`执行命令 - ${sessions.find(s => s.id === activeSession)?.name}`}
        open={commandModalVisible}
        onCancel={() => setCommandModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form layout="vertical" onFinish={handleExecuteCommand}>
          <Form.Item name="command" label="命令">
            <Input placeholder="输入命令" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              执行
            </Button>
          </Form.Item>
        </Form>
        
        <div style={{ marginTop: 20 }}>
          <Title level={5}>命令历史</Title>
          {commandHistory.map((item) => (
            <div key={item.id} style={{ marginBottom: 10, padding: 10, backgroundColor: '#f5f5f5', borderRadius: 4 }}>
              <div style={{ fontWeight: 'bold' }}>{item.command}</div>
              <div style={{ fontSize: '12px', color: '#666' }}>{item.timestamp}</div>
              <pre style={{ marginTop: 5, whiteSpace: 'pre-wrap' }}>{item.output}</pre>
            </div>
          ))}
        </div>
      </Modal>
    </div>
  );
};

export default Sessions;