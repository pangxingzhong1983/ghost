import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Select, Input, Modal, Form } from 'antd';
import { ReloadOutlined, DeleteOutlined, PlayCircleOutlined, SearchOutlined } from '@ant-design/icons';

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface Process {
  id: string;
  pid: number;
  name: string;
  user: string;
  cpu: number;
  memory: number;
  command: string;
  status: string;
  startTime: string;
}

const ProcessManager: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [processes, setProcesses] = useState<Process[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');
  const [searchText, setSearchText] = useState<string>('');
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

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

  // 获取进程列表
  const fetchProcesses = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取进程列表
      // 暂时使用模拟数据
      const mockProcesses: Process[] = [
        {
          id: '1',
          pid: 1234,
          name: 'explorer.exe',
          user: 'admin',
          cpu: 5.2,
          memory: 120.5,
          command: 'C:\\Windows\\explorer.exe',
          status: 'running',
          startTime: '2026-03-31 08:00:00'
        },
        {
          id: '2',
          pid: 5678,
          name: 'chrome.exe',
          user: 'admin',
          cpu: 12.8,
          memory: 512.3,
          command: 'C:\\Program Files\\Google\\Chrome\\chrome.exe',
          status: 'running',
          startTime: '2026-03-31 08:30:00'
        },
        {
          id: '3',
          pid: 9012,
          name: 'notepad.exe',
          user: 'admin',
          cpu: 0.1,
          memory: 15.2,
          command: 'C:\\Windows\\System32\\notepad.exe',
          status: 'running',
          startTime: '2026-03-31 09:00:00'
        }
      ];
      setProcesses(mockProcesses);
      message.success('获取进程列表成功');
    } catch (error) {
      console.error('Error fetching processes:', error);
      message.error('获取进程列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 终止进程
  const handleKillProcess = async (pid: number) => {
    try {
      // 这里应该调用WebSocket服务终止进程
      message.success(`正在终止进程 ${pid}...`);
      // 模拟终止成功
      setTimeout(() => {
        setProcesses(processes.filter(p => p.pid !== pid));
        message.success(`进程 ${pid} 已终止`);
      }, 1000);
    } catch (error) {
      console.error('Error killing process:', error);
      message.error('终止进程失败');
    }
  };

  // 启动进程
  const handleStartProcess = async (values: any) => {
    try {
      // 这里应该调用WebSocket服务启动进程
      message.success(`正在启动进程 ${values.command}...`);
      // 模拟启动成功
      setTimeout(() => {
        const newProcess: Process = {
          id: (processes.length + 1).toString(),
          pid: Math.floor(Math.random() * 10000),
          name: values.command.split('\\').pop() || values.command,
          user: 'admin',
          cpu: 0.0,
          memory: 5.0,
          command: values.command,
          status: 'running',
          startTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
        };
        setProcesses([...processes, newProcess]);
        message.success('进程启动成功');
        setModalVisible(false);
      }, 1000);
    } catch (error) {
      console.error('Error starting process:', error);
      message.error('启动进程失败');
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleSessionChange = (sessionId: string) => {
    setSelectedSession(sessionId);
    if (sessionId) {
      fetchProcesses();
    }
  };

  // 过滤进程
  const filteredProcesses = processes.filter(process => 
    process.name.toLowerCase().includes(searchText.toLowerCase()) ||
    process.command.toLowerCase().includes(searchText.toLowerCase())
  );

  const columns = [
    {
      title: 'PID',
      dataIndex: 'pid',
      key: 'pid',
    },
    {
      title: '进程名',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '用户',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: 'CPU (%)',
      dataIndex: 'cpu',
      key: 'cpu',
    },
    {
      title: '内存 (MB)',
      dataIndex: 'memory',
      key: 'memory',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '启动时间',
      dataIndex: 'startTime',
      key: 'startTime',
    },
    {
      title: '命令',
      dataIndex: 'command',
      key: 'command',
      ellipsis: true,
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Process) => (
        <Space size="middle">
          <Button 
            danger 
            icon={<DeleteOutlined />} 
            size="small" 
            onClick={() => handleKillProcess(record.pid)}
          >
            终止
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="进程管理" 
        extra={
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={fetchSessions}
              loading={loading}
            >
              刷新会话
            </Button>
            <Button 
              type="primary" 
              icon={<PlayCircleOutlined />} 
              onClick={() => setModalVisible(true)}
              disabled={!selectedSession}
            >
              启动进程
            </Button>
          </Space>
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

        <Input 
          placeholder="搜索进程" 
          prefix={<SearchOutlined />}
          style={{ marginBottom: 16, width: 300 }}
          onChange={(e) => setSearchText(e.target.value)}
        />

        <Table 
          columns={columns} 
          dataSource={filteredProcesses} 
          rowKey="id" 
          pagination={{ pageSize: 20 }}
        />
      </Card>

      <Modal
        title="启动进程"
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => setModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleStartProcess}
        >
          <Form.Item
            name="command"
            label="命令"
            rules={[{ required: true, message: '请输入命令' }]}
          >
            <Input placeholder="请输入要执行的命令" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ProcessManager;