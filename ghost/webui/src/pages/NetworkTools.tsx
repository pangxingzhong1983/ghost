import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Select, Form, Modal, Tag, Input, Descriptions } from 'antd';
import { ReloadOutlined, PlayCircleOutlined } from '@ant-design/icons';

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface NetworkResult {
  id: string;
  sessionId: string;
  tool: string;
  target: string;
  result: string;
  status: string;
  timestamp: string;
  details?: any;
}

const NetworkTools: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [results, setResults] = useState<NetworkResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');
  const [selectedTool, setSelectedTool] = useState<string>('');
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

  // 执行网络工具
  const handleExecuteTool = async (values: any) => {
    try {
      // 这里应该调用WebSocket服务执行网络工具
      message.success(`正在执行 ${selectedTool}...`);
      // 模拟执行成功
      setTimeout(() => {
        const newResult: NetworkResult = {
          id: (results.length + 1).toString(),
          sessionId: selectedSession,
          tool: selectedTool,
          target: values.target,
          result: '执行成功',
          status: 'success',
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
          details: {
            output: `工具 ${selectedTool} 执行成功\n目标: ${values.target}`,
            ports: [
              { port: 22, status: 'open', service: 'ssh' },
              { port: 80, status: 'open', service: 'http' },
              { port: 443, status: 'open', service: 'https' }
            ]
          }
        };
        setResults([newResult, ...results]);
        message.success(`${selectedTool} 执行成功`);
        setModalVisible(false);
      }, 1500);
    } catch (error) {
      console.error('Error executing tool:', error);
      message.error('执行工具失败');
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const tools = [
    { value: 'port_scan', label: '端口扫描', requiresTarget: true },
    { value: 'netstat', label: '网络状态', requiresTarget: false },
    { value: 'netmon', label: '网络监控', requiresTarget: false },
    { value: 'nbnsspoof', label: 'NBNS欺骗', requiresTarget: true },
    { value: 'tcpdump', label: '网络抓包', requiresTarget: false },
    { value: 'socks5proxy', label: 'SOCKS5代理', requiresTarget: false },
    { value: 'portfwd', label: '端口转发', requiresTarget: true }
  ];

  const currentTool = tools.find(t => t.value === selectedTool);

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
        return <Tag color="green">{toolName}</Tag>;
      },
    },
    {
      title: '目标',
      dataIndex: 'target',
      key: 'target',
    },
    {
      title: '结果',
      dataIndex: 'result',
      key: 'result',
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
      render: (_: any, record: NetworkResult) => (
        <Button 
          type="link" 
          onClick={() => {
            Modal.info({
              title: `工具执行详情 - ${tools.find(t => t.value === record.tool)?.label || record.tool}`,
              content: (
                <Descriptions bordered>
                  <Descriptions.Item label="会话ID">{record.sessionId}</Descriptions.Item>
                  <Descriptions.Item label="目标">{record.target}</Descriptions.Item>
                  <Descriptions.Item label="执行时间">{record.timestamp}</Descriptions.Item>
                  <Descriptions.Item label="结果" span={2}>{record.result}</Descriptions.Item>
                  {record.details && (
                    <>
                      <Descriptions.Item label="输出" span={2}>
                        <pre style={{ whiteSpace: 'pre-wrap' }}>{record.details.output}</pre>
                      </Descriptions.Item>
                      {record.details.ports && (
                        <Descriptions.Item label="开放端口" span={2}>
                          <Table 
                            columns={[
                              { title: '端口', dataIndex: 'port', key: 'port' },
                              { title: '状态', dataIndex: 'status', key: 'status' },
                              { title: '服务', dataIndex: 'service', key: 'service' }
                            ]} 
                            dataSource={record.details.ports} 
                            rowKey="port" 
                            pagination={false}
                          />
                        </Descriptions.Item>
                      )}
                    </>
                  )}
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
        title="网络工具" 
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
            执行工具
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
        title={`执行工具 - ${tools.find(t => t.value === selectedTool)?.label || selectedTool}`}
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => setModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleExecuteTool}
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
          {currentTool?.requiresTarget && (
            <Form.Item
              name="target"
              label="目标"
              rules={[{ required: true, message: '请输入目标' }]}
            >
              <Input placeholder="请输入目标IP或域名" />
            </Form.Item>
          )}
        </Form>
      </Modal>
    </div>
  );
};

export default NetworkTools;