import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Modal, Image } from 'antd';
import { MonitorOutlined, LockOutlined, ReloadOutlined, DownloadOutlined } from '@ant-design/icons';

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface Screenshot {
  id: string;
  sessionId: string;
  timestamp: string;
  imageUrl: string;
  resolution: string;
}

const ScreenControl: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [screenshots, setScreenshots] = useState<Screenshot[]>([]);
  const [loading, setLoading] = useState(false);
  const [screenshotLoading, setScreenshotLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [currentScreenshot, setCurrentScreenshot] = useState<string>('');

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

  // 截取屏幕
  const handleScreenshot = async (sessionId: string) => {
    setScreenshotLoading(true);
    try {
      // 这里应该调用WebSocket服务执行屏幕截图
      message.success('正在截取屏幕...');
      // 模拟截图成功
      setTimeout(() => {
        const newScreenshot: Screenshot = {
          id: (screenshots.length + 1).toString(),
          sessionId,
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
          imageUrl: `https://picsum.photos/800/600?random=${Math.random()}`,
          resolution: '1920x1080'
        };
        setScreenshots([newScreenshot, ...screenshots]);
        message.success('屏幕截图成功');
        setScreenshotLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error taking screenshot:', error);
      message.error('屏幕截图失败');
      setScreenshotLoading(false);
    }
  };

  // 锁定屏幕
  const handleLockScreen = async () => {
    try {
      // 这里应该调用WebSocket服务锁定屏幕
      message.success('正在锁定屏幕...');
      // 模拟锁定成功
      setTimeout(() => {
        message.success('屏幕锁定成功');
      }, 1000);
    } catch (error) {
      console.error('Error locking screen:', error);
      message.error('屏幕锁定失败');
    }
  };

  // 显示屏幕
  const handleShowScreen = async (screenshot: Screenshot) => {
    setCurrentScreenshot(screenshot.imageUrl);
    setModalVisible(true);
  };

  // 下载截图
  const handleDownloadScreenshot = (screenshot: Screenshot) => {
    const link = document.createElement('a');
    link.href = screenshot.imageUrl;
    link.download = `screenshot-${screenshot.timestamp.replace(/:/g, '-')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    message.success('截图下载成功');
  };

  // 刷新截图列表
  const refreshScreenshots = async () => {
    // 这里应该调用WebSocket服务获取截图列表
    message.success('截图列表已刷新');
  };

  useEffect(() => {
    fetchSessions();
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
      title: '最后 seen',
      dataIndex: 'lastSeen',
      key: 'lastSeen',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Session) => (
        <Space size="middle">
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            size="small" 
            onClick={() => handleScreenshot(record.id)}
            loading={screenshotLoading}
            disabled={record.status !== 'active'}
          >
            截图
          </Button>
          <Button 
            icon={<LockOutlined />} 
            size="small" 
            onClick={() => handleLockScreen()}
            disabled={record.status !== 'active'}
          >
            锁定
          </Button>
        </Space>
      ),
    },
  ];

  const screenshotColumns = [
    {
      title: '会话ID',
      dataIndex: 'sessionId',
      key: 'sessionId',
    },
    {
      title: '时间戳',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Screenshot, b: Screenshot) => a.timestamp.localeCompare(b.timestamp),
      defaultSortOrder: 'descend' as const,
    },
    {
      title: '分辨率',
      dataIndex: 'resolution',
      key: 'resolution',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Screenshot) => (
        <Space size="middle">
          <Button 
            icon={<MonitorOutlined />} 
            size="small" 
            onClick={() => handleShowScreen(record)}
          >
            查看
          </Button>
          <Button 
            icon={<DownloadOutlined />} 
            size="small" 
            onClick={() => handleDownloadScreenshot(record)}
          >
            下载
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="屏幕控制" 
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
        <h3>可用会话</h3>
        <Table 
          columns={sessionColumns} 
          dataSource={sessions} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
          style={{ marginBottom: 24 }}
        />

        <h3>屏幕截图</h3>
        <Button 
          icon={<ReloadOutlined />} 
          onClick={refreshScreenshots}
          style={{ marginBottom: 16 }}
        >
          刷新截图
        </Button>
        <Table 
          columns={screenshotColumns} 
          dataSource={screenshots} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="屏幕截图"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        width={800}
        footer={[
          <Button key="close" onClick={() => setModalVisible(false)}>
            关闭
          </Button>
        ]}
      >
        {currentScreenshot && (
          <Image 
            src={currentScreenshot} 
            alt="屏幕截图" 
            style={{ width: '100%' }}
          />
        )}
      </Modal>
    </div>
  );
};

export default ScreenControl;