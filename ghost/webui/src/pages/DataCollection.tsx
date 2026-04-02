import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Space, Select, Form, Modal, Tag, Descriptions } from 'antd';
import { ReloadOutlined, PlayCircleOutlined, DownloadOutlined } from '@ant-design/icons';

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface DataResult {
  id: string;
  sessionId: string;
  tool: string;
  result: string;
  status: string;
  timestamp: string;
  dataCount?: number;
  details?: any;
}

const DataCollection: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [results, setResults] = useState<DataResult[]>([]);
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

  // 执行数据收集工具
  const handleExecuteTool = async () => {
    try {
      // 这里应该调用WebSocket服务执行数据收集工具
      message.success(`正在执行 ${selectedTool}...`);
      // 模拟执行成功
      setTimeout(() => {
        const newResult: DataResult = {
          id: (results.length + 1).toString(),
          sessionId: selectedSession,
          tool: selectedTool,
          result: '执行成功',
          status: 'success',
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
          dataCount: Math.floor(Math.random() * 20) + 1,
          details: {
            output: `工具 ${selectedTool} 执行成功\n收集到 ${Math.floor(Math.random() * 20) + 1} 条数据`,
            sample: '收集的数据样本...'
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

  // 下载数据
  const handleDownloadData = () => {
    message.success('正在下载数据...');
    setTimeout(() => {
      message.success('数据下载成功');
    }, 1000);
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const tools = [
    { value: 'credcap', label: '凭证捕获' },
    { value: 'creddump', label: '凭证转储' },
    { value: 'lazagne', label: '密码获取' },
    { value: 'netcreds', label: '网络凭证' },
    { value: 'loot_memory', label: '内存数据提取' },
    { value: 'webcamsnap', label: '摄像头快照' },
    { value: 'record_mic', label: '麦克风录音' }
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
        return <Tag color="purple">{toolName}</Tag>;
      },
    },
    {
      title: '收集数据量',
      dataIndex: 'dataCount',
      key: 'dataCount',
      render: (count: number) => count || 0,
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
      render: (_: any, record: DataResult) => (
        <Space size="middle">
          <Button 
            icon={<DownloadOutlined />} 
            size="small" 
            onClick={() => handleDownloadData()}
          >
            下载
          </Button>
          <Button 
            type="link" 
            onClick={() => {
              Modal.info({
                title: `工具执行详情 - ${tools.find(t => t.value === record.tool)?.label || record.tool}`,
                content: (
                  <Descriptions bordered>
                    <Descriptions.Item label="会话ID">{record.sessionId}</Descriptions.Item>
                    <Descriptions.Item label="收集数据量">{record.dataCount || 0}</Descriptions.Item>
                    <Descriptions.Item label="执行时间">{record.timestamp}</Descriptions.Item>
                    <Descriptions.Item label="结果" span={2}>{record.result}</Descriptions.Item>
                    {record.details && (
                      <>
                        <Descriptions.Item label="输出" span={2}>
                          <pre style={{ whiteSpace: 'pre-wrap' }}>{record.details.output}</pre>
                        </Descriptions.Item>
                        {record.details.sample && (
                          <Descriptions.Item label="样本" span={2}>{record.details.sample}</Descriptions.Item>
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
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card 
        title="数据收集" 
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
        </Form>
      </Modal>
    </div>
  );
};

export default DataCollection;