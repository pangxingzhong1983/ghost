import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Select, Descriptions, Tag, Typography } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

const { Text } = Typography;

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface SystemInfo {
  sessionId: string;
  hostname: string;
  os: string;
  arch: string;
  kernel: string;
  uptime: string;
  cpu: string;
  memory: string;
  disk: string;
  network: Array<{
    interface: string;
    ip: string;
    mac: string;
  }>;
  users: Array<{
    name: string;
    uid: string;
    gid: string;
    home: string;
    shell: string;
  }>;
  timestamp: string;
}

const SystemInfo: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');

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

  // 获取系统信息
  const fetchSystemInfo = async (sessionId: string) => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取系统信息
      // 暂时使用模拟数据
      const mockSystemInfo: SystemInfo = {
        sessionId,
        hostname: 'WIN10-PC',
        os: 'Windows 10 Pro 22H2',
        arch: 'x64',
        kernel: '10.0.19045',
        uptime: '2 days, 14:30:45',
        cpu: 'Intel(R) Core(TM) i7-8700K @ 3.70GHz',
        memory: '16 GB (8 GB used)',
        disk: '512 GB SSD (200 GB used)',
        network: [
          {
            interface: 'Ethernet',
            ip: '192.168.1.100',
            mac: '00:11:22:33:44:55'
          },
          {
            interface: 'Wi-Fi',
            ip: '192.168.1.101',
            mac: 'AA:BB:CC:DD:EE:FF'
          }
        ],
        users: [
          {
            name: 'admin',
            uid: '1000',
            gid: '1000',
            home: 'C:\\Users\\admin',
            shell: 'cmd.exe'
          },
          {
            name: 'user',
            uid: '1001',
            gid: '1001',
            home: 'C:\\Users\\user',
            shell: 'cmd.exe'
          }
        ],
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
      };
      setSystemInfo(mockSystemInfo);
      message.success('获取系统信息成功');
    } catch (error) {
      console.error('Error fetching system info:', error);
      message.error('获取系统信息失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleSessionChange = (sessionId: string) => {
    setSelectedSession(sessionId);
    if (sessionId) {
      fetchSystemInfo(sessionId);
    }
  };

  return (
    <div>
      <Card 
        title="系统信息" 
        extra={
          <Button 
            icon={<ReloadOutlined />} 
            onClick={fetchSessions}
            loading={loading}
          >
            刷新会话
          </Button>
        }
      >
        <div style={{ marginBottom: 16 }}>
          <span style={{ marginRight: 8 }}>选择会话：</span>
          <Select 
            style={{ width: 300 }}
            placeholder="请选择会话"
            onChange={handleSessionChange}
            value={selectedSession}
          >
            {sessions.map(session => (
              <Option key={session.id} value={session.id}>
                {session.name} ({session.ip}) - {session.platform}
              </Option>
            ))}
          </Select>
        </div>

        {systemInfo && (
          <div>
            <Descriptions bordered column={2}>
              <Descriptions.Item label="主机名" span={2}>
                <Tag color="blue">{systemInfo.hostname}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="操作系统">{systemInfo.os}</Descriptions.Item>
              <Descriptions.Item label="架构">{systemInfo.arch}</Descriptions.Item>
              <Descriptions.Item label="内核版本">{systemInfo.kernel}</Descriptions.Item>
              <Descriptions.Item label="运行时间">{systemInfo.uptime}</Descriptions.Item>
              <Descriptions.Item label="CPU">{systemInfo.cpu}</Descriptions.Item>
              <Descriptions.Item label="内存">{systemInfo.memory}</Descriptions.Item>
              <Descriptions.Item label="磁盘">{systemInfo.disk}</Descriptions.Item>
            </Descriptions>

            <h3 style={{ marginTop: 24 }}>网络信息</h3>
            <Table 
              columns={[
                { title: '接口', dataIndex: 'interface', key: 'interface' },
                { title: 'IP地址', dataIndex: 'ip', key: 'ip' },
                { title: 'MAC地址', dataIndex: 'mac', key: 'mac' }
              ]} 
              dataSource={systemInfo.network} 
              rowKey="interface" 
              pagination={false}
            />

            <h3 style={{ marginTop: 24 }}>用户信息</h3>
            <Table 
              columns={[
                { title: '用户名', dataIndex: 'name', key: 'name' },
                { title: 'UID', dataIndex: 'uid', key: 'uid' },
                { title: 'GID', dataIndex: 'gid', key: 'gid' },
                { title: '主目录', dataIndex: 'home', key: 'home' },
                { title: 'Shell', dataIndex: 'shell', key: 'shell' }
              ]} 
              dataSource={systemInfo.users} 
              rowKey="name" 
              pagination={false}
            />

            <div style={{ marginTop: 16, textAlign: 'right' }}>
              <Text type="secondary">最后更新：{systemInfo.timestamp}</Text>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default SystemInfo;