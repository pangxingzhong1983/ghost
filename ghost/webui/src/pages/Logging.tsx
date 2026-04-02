import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Select, Input, Tag, Typography } from 'antd';
import { ReloadOutlined, DownloadOutlined, ClearOutlined, SearchOutlined } from '@ant-design/icons';

const { Option } = Select;
const { Text } = Typography;

interface LogEntry {
  id: string;
  timestamp: string;
  level: string;
  source: string;
  message: string;
  details?: string;
}

const Logging: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterLevel, setFilterLevel] = useState<string>('all');
  const [filterSource, setFilterSource] = useState<string>('all');
  const [searchText, setSearchText] = useState<string>('');

  // 获取日志列表
  const fetchLogs = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取日志列表
      // 暂时使用模拟数据
      const mockLogs: LogEntry[] = [
        {
          id: '1',
          timestamp: '2026-03-31 10:00:00',
          level: 'info',
          source: 'server',
          message: 'Server started successfully',
          details: 'Ghost C2 server started on port 4444'
        },
        {
          id: '2',
          timestamp: '2026-03-31 10:05:00',
          level: 'warning',
          source: 'listener',
          message: 'Listener port 8080 already in use',
          details: 'Attempting to use alternative port 8081'
        },
        {
          id: '3',
          timestamp: '2026-03-31 10:10:00',
          level: 'error',
          source: 'payload',
          message: 'Failed to generate payload',
          details: 'Invalid configuration parameters'
        },
        {
          id: '4',
          timestamp: '2026-03-31 10:15:00',
          level: 'info',
          source: 'session',
          message: 'New session established',
          details: 'Session ID: 12345, IP: 192.168.1.100'
        },
        {
          id: '5',
          timestamp: '2026-03-31 10:20:00',
          level: 'info',
          source: 'server',
          message: 'Server shutdown',
          details: 'Received SIGINT signal'
        }
      ];
      setLogs(mockLogs);
      message.success('获取日志列表成功');
    } catch (error) {
      console.error('Error fetching logs:', error);
      message.error('获取日志列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 过滤日志
  const filteredLogs = logs.filter(log => {
    const levelMatch = filterLevel === 'all' || log.level === filterLevel;
    const sourceMatch = filterSource === 'all' || log.source === filterSource;
    const searchMatch = searchText === '' || 
      log.message.toLowerCase().includes(searchText.toLowerCase()) ||
      (log.details && log.details.toLowerCase().includes(searchText.toLowerCase()));
    return levelMatch && sourceMatch && searchMatch;
  });

  // 下载日志
  const handleDownload = () => {
    const logContent = filteredLogs.map(log => {
      return `${log.timestamp} [${log.level.toUpperCase()}] [${log.source}] ${log.message}${log.details ? ' - ' + log.details : ''}`;
    }).join('\n');

    const blob = new Blob([logContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ghost-logs-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    message.success('日志下载成功');
  };

  // 清除日志
  const handleClear = async () => {
    try {
      // 这里应该调用WebSocket服务清除日志
      setLogs([]);
      message.success('日志清除成功');
    } catch (error) {
      console.error('Error clearing logs:', error);
      message.error('日志清除失败');
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const columns = [
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: LogEntry, b: LogEntry) => a.timestamp.localeCompare(b.timestamp),
      defaultSortOrder: 'descend' as const,
    },
    {
      title: '级别',
      dataIndex: 'level',
      key: 'level',
      render: (level: string) => {
        let color = '';
        switch (level) {
          case 'error':
            color = 'red';
            break;
          case 'warning':
            color = 'orange';
            break;
          case 'info':
            color = 'blue';
            break;
          default:
            color = 'gray';
        }
        return <Tag color={color}>{level.toUpperCase()}</Tag>;
      },
    },
    {
      title: '来源',
      dataIndex: 'source',
      key: 'source',
      render: (source: string) => <Tag color="green">{source}</Tag>,
    },
    {
      title: '消息',
      dataIndex: 'message',
      key: 'message',
    },
    {
      title: '详情',
      dataIndex: 'details',
      key: 'details',
      render: (details: string) => details ? (
        <Text type="secondary">{details}</Text>
      ) : (
        <Text type="secondary">无</Text>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="日志管理" 
        extra={
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={fetchLogs}
              loading={loading}
            >
              刷新
            </Button>
            <Button 
              icon={<DownloadOutlined />} 
              onClick={handleDownload}
              disabled={filteredLogs.length === 0}
            >
              下载
            </Button>
            <Button 
              danger 
              icon={<ClearOutlined />} 
              onClick={handleClear}
              disabled={logs.length === 0}
            >
              清除
            </Button>
          </Space>
        }
      >
        <Space style={{ marginBottom: 16 }}>
          <Select 
            defaultValue="all" 
            onChange={setFilterLevel}
            style={{ width: 120 }}
          >
            <Option value="all">所有级别</Option>
            <Option value="info">Info</Option>
            <Option value="warning">Warning</Option>
            <Option value="error">Error</Option>
          </Select>
          <Select 
            defaultValue="all" 
            onChange={setFilterSource}
            style={{ width: 120 }}
          >
            <Option value="all">所有来源</Option>
            <Option value="server">Server</Option>
            <Option value="listener">Listener</Option>
            <Option value="payload">Payload</Option>
            <Option value="session">Session</Option>
          </Select>
          <Input 
            placeholder="搜索日志" 
            prefix={<SearchOutlined />}
            style={{ width: 300 }}
            onChange={(e) => setSearchText(e.target.value)}
          />
        </Space>
        <Table 
          columns={columns} 
          dataSource={filteredLogs} 
          rowKey="id" 
          pagination={{ pageSize: 20 }}
        />
      </Card>
    </div>
  );
};

export default Logging;