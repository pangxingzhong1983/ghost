import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Select, Form, Modal, Tag, Input, Descriptions } from 'antd';
import { PlayCircleOutlined, ReloadOutlined } from '@ant-design/icons';

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface ExecutionResult {
  id: string;
  sessionId: string;
  tool: string;
  command: string;
  output: string;
  status: string;
  timestamp: string;
}

const ExecutionTools: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [results, setResults] = useState<ExecutionResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');
  const [selectedTool, setSelectedTool] = useState<string>('');
  const [command, setCommand] = useState<string>('');
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

  // 执行命令
  const handleExecuteCommand = async (values: any) => {
    try {
      // 这里应该调用WebSocket服务执行命令
      message.success(`正在执行 ${selectedTool} 命令...`);
      // 模拟执行成功
      setTimeout(() => {
        const newResult: ExecutionResult = {
          id: (results.length + 1).toString(),
          sessionId: selectedSession,
          tool: selectedTool,
          command: values.command,
          output: `命令执行成功\n输出: This is a mock output for ${selectedTool} command\n${values.command}`,
          status: 'success',
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
        };
        setResults([newResult, ...results]);
        message.success(`${selectedTool} 命令执行成功`);
        setModalVisible(false);
      }, 1500);
    } catch (error) {
      console.error('Error executing command:', error);
      message.error('执行命令失败');
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const tools = [
    { value: 'powershell', label: 'PowerShell执行' },
    { value: 'pyexec', label: 'Python执行' },
    { value: 'shell_exec', label: 'Shell执行' },
    { value: 'interactive_shell', label: '交互式Shell' },
    { value: 'psh', label: 'PowerShell执行' },
    { value: 'pyshell', label: 'Python Shell' },
    { value: 'sshell', label: '反向Shell' },
    { value: 'rdp', label: 'RDP管理' },
    { value: 'rdesktop', label: '远程桌面' },
    { value: 'ssh', label: 'SSH连接' },
    { value: 'psexec', label: 'PsExec执行' },
    { value: 'wmiexec', label: 'WMI执行' },
    { value: 'dcomexec', label: 'DCOM执行' },
    { value: 'atexec', label: '计划任务执行' }
  ];

  const columns = [
    {
      title: '会话ID',
      dataIndex: 'sessionId',
      key: 'sessionId',
    },
    {
      title: '工具',
      dataIndex: 'tool',
      key: 'tool',
      render: (tool: string) => {
        const toolName = tools.find(t => t.value === tool)?.label || tool;
        return <Tag color="cyan">{toolName}</Tag>;
      },
    },
    {
      title: '命令',
      dataIndex: 'command',
      key: 'command',
      ellipsis: true,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'success' ? 'green' : 'red'}>
          {status === 'success' ? '成功' : '失败'}
        </Tag>
      ),
    },
    {
      title: '执行时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: ExecutionResult) => (
        <Button 
          type="link" 
          onClick={() => {
            Modal.info({
              title: `命令执行详情 - ${tools.find(t => t.value === record.tool)?.label || record.tool}`,
              content: (
                <Descriptions bordered>
                  <Descriptions.Item label="会话ID">{record.sessionId}</Descriptions.Item>
                  <Descriptions.Item label="命令" span={2}>{record.command}</Descriptions.Item>
                  <Descriptions.Item label="执行时间">{record.timestamp}</Descriptions.Item>
                  <Descriptions.Item label="状态">
                    <Tag color={record.status === 'success' ? 'green' : 'red'}>
                      {record.status === 'success' ? '成功' : '失败'}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="输出" span={2}>
                    <pre style={{ whiteSpace: 'pre-wrap', maxHeight: '300px', overflow: 'auto' }}>
                      {record.output}
                    </pre>
                  </Descriptions.Item>
                </Descriptions>
              ),
            });
          }}
        >
          查看详情
        </Button>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="执行工具" 
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
            style={{ width: 200, marginRight: 16 }}
            placeholder="请选择会话"
            onChange={setSelectedSession}
            value={selectedSession}
          >
            {sessions.map(session => (
              <Option key={session.id} value={session.id}>
                {session.name} ({session.ip})
              </Option>
            ))}
          </Select>
          <span style={{ marginRight: 8 }}>选择工具：</span>
          <Select 
            style={{ width: 200, marginRight: 16 }}
            placeholder="请选择工具"
            onChange={setSelectedTool}
            value={selectedTool}
          >
            {tools.map(tool => (
              <Option key={tool.value} value={tool.value}>{tool.label}</Option>
            ))}
          </Select>
          <Button 
            type="primary" 
            icon={<PlayCircleOutlined />} 
            onClick={() => setModalVisible(true)}
            disabled={!selectedSession || !selectedTool}
          >
            执行命令
          </Button>
        </div>

        <Table 
          columns={columns} 
          dataSource={results} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={`执行命令 - ${tools.find(t => t.value === selectedTool)?.label || selectedTool}`}
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => setModalVisible(false)}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleExecuteCommand}
        >
          <Form.Item
            label="会话"
          >
            <Select 
              style={{ width: '100%' }}
              value={selectedSession}
              disabled
            >
              {sessions.map(session => (
                <Option key={session.id} value={session.id}>
                  {session.name} ({session.ip})
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            label="工具"
          >
            <Select 
              style={{ width: '100%' }}
              value={selectedTool}
              disabled
            >
              {tools.map(tool => (
                <Option key={tool.value} value={tool.value}>{tool.label}</Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="command"
            label="命令"
            rules={[{ required: true, message: '请输入命令' }]}
          >
            <Input.TextArea 
              rows={4} 
              placeholder="请输入要执行的命令"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ExecutionTools;