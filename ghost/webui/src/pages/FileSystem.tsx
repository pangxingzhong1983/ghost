import React, { useState, useEffect } from 'react';
import { Card, Button, Table, message, Select, Form, Modal, Tag, Input, Tree } from 'antd';
import { FolderOutlined, FileOutlined, ReloadOutlined, UploadOutlined, DeleteOutlined, EditOutlined, PlusOutlined } from '@ant-design/icons';

const { Option } = Select;

interface Session {
  id: string;
  name: string;
  ip: string;
  platform: string;
  status: string;
  lastSeen: string;
}

interface File {
  key: string;
  title: string;
  type: 'file' | 'directory';
  path: string;
  size?: number;
  modified?: string;
  children?: File[];
}

interface FileSystemResult {
  id: string;
  sessionId: string;
  action: string;
  path: string;
  result: string;
  status: string;
  timestamp: string;
}

const FileSystem: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<FileSystemResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');
  const [currentPath, setCurrentPath] = useState<string>('/');
  const [modalVisible, setModalVisible] = useState(false);
  const [modalType, setModalType] = useState<'create' | 'delete' | 'edit'>('create');

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

  // 获取文件列表
  const fetchFiles = async () => {
    setLoading(true);
    try {
      // 这里应该调用WebSocket服务获取文件列表
      // 暂时使用模拟数据
      const mockFiles: File[] = [
        {
          key: '1',
          title: 'Documents',
          type: 'directory',
          path: currentPath + 'Documents/',
          children: [
            {
              key: '1-1',
              title: 'report.docx',
              type: 'file',
              path: currentPath + 'Documents/report.docx',
              size: 102400,
              modified: '2026-03-30 15:30:00'
            },
            {
              key: '1-2',
              title: 'notes.txt',
              type: 'file',
              path: currentPath + 'Documents/notes.txt',
              size: 2048,
              modified: '2026-03-31 10:00:00'
            }
          ]
        },
        {
          key: '2',
          title: 'Downloads',
          type: 'directory',
          path: currentPath + 'Downloads/',
          children: [
            {
              key: '2-1',
              title: 'installer.exe',
              type: 'file',
              path: currentPath + 'Downloads/installer.exe',
              size: 5120000,
              modified: '2026-03-29 09:15:00'
            }
          ]
        },
        {
          key: '3',
          title: 'desktop.ini',
          type: 'file',
          path: currentPath + 'desktop.ini',
          size: 512,
          modified: '2026-03-28 14:20:00'
        }
      ];
      setFiles(mockFiles);
      message.success('获取文件列表成功');
    } catch (error) {
      console.error('Error fetching files:', error);
      message.error('获取文件列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 执行文件操作
  const handleFileAction = async (action: string, path: string) => {
    try {
      // 这里应该调用WebSocket服务执行文件操作
      message.success(`正在执行 ${action}...`);
      // 模拟执行成功
      setTimeout(() => {
        const newResult: FileSystemResult = {
          id: (results.length + 1).toString(),
          sessionId: selectedSession,
          action,
          path,
          result: '执行成功',
          status: 'success',
          timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19)
        };
        setResults([newResult, ...results]);
        message.success(`${action} 执行成功`);
        setModalVisible(false);
        // 刷新文件列表
        fetchFiles();
      }, 1000);
    } catch (error) {
      console.error('Error executing file action:', error);
      message.error('执行操作失败');
    }
  };



  useEffect(() => {
    fetchSessions();
  }, []);

  const handleSessionChange = (sessionId: string) => {
    setSelectedSession(sessionId);
    if (sessionId) {
      fetchFiles();
    }
  };

  const handleNodeClick = (node: any) => {
    if (node.type === 'directory') {
      setCurrentPath(node.path);
      fetchFiles();
    }
  };

  const renderTreeNodes = (data: File[]) => {
    return data.map(item => {
      const icon = item.type === 'directory' ? <FolderOutlined /> : <FileOutlined />;
      if (item.children) {
        return (
          <Tree.TreeNode title={item.title} key={item.key} icon={icon}>
            {renderTreeNodes(item.children)}
          </Tree.TreeNode>
        );
      }
      return <Tree.TreeNode title={item.title} key={item.key} icon={icon} />;
    });
  };

  const columns = [
    {
      title: '操作',
      dataIndex: 'action',
      key: 'action',
    },
    {
      title: '路径',
      dataIndex: 'path',
      key: 'path',
      ellipsis: true,
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
  ];

  return (
    <div>
      <Card 
        title="文件系统" 
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
            onChange={handleSessionChange}
            value={selectedSession}
          >
            {sessions.map(session => (
              <Option key={session.id} value={session.id}>
                {session.name} ({session.ip})
              </Option>
            ))}
          </Select>
          <span style={{ marginRight: 8 }}>当前路径：</span>
          <Input 
            style={{ width: 300 }} 
            value={currentPath} 
            disabled
          />
        </div>

        <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
          <Button 
            icon={<PlusOutlined />} 
            onClick={() => {
              setModalType('create');
              setModalVisible(true);
            }}
            disabled={!selectedSession}
          >
            创建目录
          </Button>
          <Button 
            icon={<UploadOutlined />} 
            onClick={() => {
              // 这里可以实现上传文件的逻辑
              message.info('上传功能待实现');
            }}
            disabled={!selectedSession}
          >
            上传文件
          </Button>
          <Button 
            icon={<DeleteOutlined />} 
            danger
            onClick={() => {
              setModalType('delete');
              setModalVisible(true);
            }}
            disabled={!selectedSession}
          >
            删除
          </Button>
          <Button 
            icon={<EditOutlined />} 
            onClick={() => {
              setModalType('edit');
              setModalVisible(true);
            }}
            disabled={!selectedSession}
          >
            编辑
          </Button>
        </div>

        <div style={{ display: 'flex', gap: 24 }}>
          <div style={{ flex: 1 }}>
            <h3>文件树</h3>
            <Tree
              onSelect={() => {
              // 由于我们移除了dataRef，这里暂时不设置selectedFile
            }}
              onExpand={() => {}}
              onDoubleClick={handleNodeClick}
              treeData={files}
            />
          </div>
          <div style={{ flex: 2 }}>
            <h3>操作历史</h3>
            <Table 
              columns={columns} 
              dataSource={results} 
              rowKey="id" 
              pagination={{ pageSize: 10 }}
            />
          </div>
        </div>
      </Card>

      <Modal
        title={
          modalType === 'create' ? '创建目录' :
          modalType === 'delete' ? '删除文件/目录' : '编辑文件'
        }
        open={modalVisible}
        onOk={() => {
          if (modalType === 'create') {
            form.submit();
          } else if (modalType === 'delete') {
            handleFileAction('删除', currentPath);
          }
        }}
        onCancel={() => setModalVisible(false)}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={(values) => {
            if (modalType === 'create') {
              handleFileAction('创建目录', currentPath + values.name);
            }
          }}
        >
          {modalType === 'create' && (
            <Form.Item
              name="name"
              label="目录名称"
              rules={[{ required: true, message: '请输入目录名称' }]}
            >
              <Input placeholder="请输入目录名称" />
            </Form.Item>
          )}
          {modalType === 'delete' && (
            <div>
              <p>确定要删除 <strong>{currentPath}</strong> 吗？</p>
              <p style={{ color: 'red' }}>此操作不可撤销！</p>
            </div>
          )}
          {modalType === 'edit' && (
            <Form.Item
              name="content"
              label="文件内容"
              rules={[{ required: true, message: '请输入文件内容' }]}
            >
              <Input.TextArea rows={8} placeholder="请输入文件内容" />
            </Form.Item>
          )}
        </Form>
      </Modal>
    </div>
  );
};

export default FileSystem;