import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Select, Form, Modal, Tag, Input, Descriptions, Tabs } from 'antd';
import { ReloadOutlined, PlayCircleOutlined } from '@ant-design/icons';

const { Option } = Select;
const { TabPane } = Tabs;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface UtilityResult {
  id: string;
  sessionId: string;
  tool: string;
  command: string;
  output: string;
  status: string;
  timestamp: string;
}

const Utilities: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [results, setResults] = useState<UtilityResult[]>([]);
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

  // 执行工具
  const handleExecuteTool = async (values: any) => {
    try {
      // 这里应该调用WebSocket服务执行工具
      message.success(`正在执行 ${selectedTool}...`);
      // 模拟执行成功
      setTimeout(() => {
        const newResult: UtilityResult = {
          id: (results.length + 1).toString(),
          sessionId: selectedSession,
          tool: selectedTool,
          command: values.command || '',
          output: `工具 ${selectedTool} 执行成功\n输出: This is a mock output for ${selectedTool}`,
          status: 'success',
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
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

  const tools = {
    activeDirectory: [
      { value: 'ad', label: '活动目录操作' },
      { value: 'getdomain', label: '获取域名' },
      { value: 'powerview', label: 'PowerView AD工具' },
      { value: 'pywerview', label: 'Python版PowerView' }
    ],
    systemInfo: [
      { value: 'alive', label: '主机存活检测' },
      { value: 'apps', label: '应用程序信息' },
      { value: 'cloudinfo', label: '云服务信息' },
      { value: 'contacts', label: '联系人信息' },
      { value: 'date', label: '日期时间' },
      { value: 'drives', label: '驱动器信息' },
      { value: 'get_hwuuid', label: '获取硬件UUID' },
      { value: 'getpid', label: '获取进程ID' },
      { value: 'getppid', label: '获取父进程ID' },
      { value: 'getprivs', label: '获取权限' },
      { value: 'getuid', label: '获取用户ID' },
      { value: 'ip', label: 'IP信息' },
      { value: 'last', label: '最近登录' },
      { value: 'mapped', label: '映射驱动器' },
      { value: 'stat', label: '文件状态' },
      { value: 'users', label: '用户管理' },
      { value: 'w', label: '显示当前用户' }
    ],
    network: [
      { value: 'dns', label: 'DNS相关' },
      { value: 'http', label: 'HTTP相关' },
      { value: 'igd', label: '互联网网关设备' },
      { value: 'shares', label: '共享管理' },
      { value: 'smb', label: 'SMB相关' },
      { value: 'smbspider', label: 'SMB爬虫' }
    ],
    security: [
      { value: 'call', label: '函数调用' },
      { value: 'duplicate', label: '复制会话' },
      { value: 'echo', label: '回显命令' },
      { value: 'env', label: '环境变量' },
      { value: 'exit', label: '退出' },
      { value: 'gpstracker', label: 'GPS追踪' },
      { value: 'hashmon', label: '哈希监控' },
      { value: 'impersonate', label: '模拟用户' },
      { value: 'isearch', label: '智能搜索' },
      { value: 'linux_stealth', label: 'Linux隐身' },
      { value: 'load_package', label: '加载包' },
      { value: 'memory_exec', label: '内存执行' },
      { value: 'memstrings', label: '内存字符串提取' },
      { value: 'migrate', label: '进程迁移' },
      { value: 'mimipy', label: 'Python版mimikatz' },
      { value: 'mimishell', label: '模拟Shell' },
      { value: 'mouselogger', label: '鼠标记录' },
      { value: 'msgbox', label: '消息框' },
      { value: 'odbc', label: 'ODBC数据库' },
      { value: 'outlook', label: 'Outlook邮件' },
      { value: 'pexec', label: '进程执行' },
      { value: 'pipecatcher', label: '管道捕获' },
      { value: 'rfs', label: '远程文件系统' },
      { value: 'rwmic', label: '远程WMI命令' },
      { value: 'scapy_shell', label: 'Scapy网络工具' },
      { value: 'shellcode_exec', label: 'Shellcode执行' },
      { value: 'sudo_alias', label: 'sudo别名' },
      { value: 'text_to_speach', label: '文本转语音' },
      { value: 'ttyrec', label: '终端录制' },
      { value: 'usniper', label: '用户狙击' },
      { value: 'vibrate', label: '振动控制' },
      { value: 'x509', label: 'X.509证书' }
    ],
    registry: [
      { value: 'reg', label: '注册表操作' }
    ],
    display: [
      { value: 'display', label: '显示设置' }
    ]
  };

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
        let toolName = tool;
        Object.values(tools).forEach(category => {
          const foundTool = category.find(t => t.value === tool);
          if (foundTool) {
            toolName = foundTool.label;
          }
        });
        return <Tag color="blue">{toolName}</Tag>;
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
      render: (_: any, record: UtilityResult) => (
        <Button 
          type="link" 
          onClick={() => {
            Modal.info({
              title: `工具执行详情`,
              content: (
                <Descriptions bordered>
                  <Descriptions.Item label="会话ID">{record.sessionId}</Descriptions.Item>
                  <Descriptions.Item label="工具">{record.tool}</Descriptions.Item>
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
        title="综合工具" 
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
        </div>

        <Tabs defaultActiveKey="activeDirectory">
          <TabPane tab="活动目录" key="activeDirectory">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.activeDirectory.map(tool => (
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
          </TabPane>

          <TabPane tab="系统信息" key="systemInfo">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.systemInfo.map(tool => (
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
          </TabPane>

          <TabPane tab="网络" key="network">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.network.map(tool => (
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
          </TabPane>

          <TabPane tab="安全" key="security">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.security.map(tool => (
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
          </TabPane>

          <TabPane tab="注册表" key="registry">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.registry.map(tool => (
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
          </TabPane>

          <TabPane tab="显示" key="display">
            <div style={{ marginBottom: 16 }}>
              <span style={{ marginRight: 8 }}>选择工具：</span>
              <Select 
                style={{ width: 200, marginRight: 16 }}
                placeholder="请选择工具"
                onChange={setSelectedTool}
                value={selectedTool}
              >
                {tools.display.map(tool => (
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
          </TabPane>
        </Tabs>

        <Table 
          columns={columns} 
          dataSource={results} 
          rowKey="id" 
          pagination={{ pageSize: 10 }}
          style={{ marginTop: 16 }}
        />
      </Card>

      <Modal
        title={`执行工具`}
        open={modalVisible}
        onOk={() => form.submit()}
        onCancel={() => setModalVisible(false)}
        width={800}
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
              {Object.values(tools).flat().map(tool => (
                <Option key={tool.value} value={tool.value}>{tool.label}</Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="command"
            label="命令"
            rules={[{ required: false }]}
          >
            <Input.TextArea 
              rows={4} 
              placeholder="请输入要执行的命令（可选）"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Utilities;