import React, { useState } from 'react';
import { Card, Typography, Spin, Table, Button, Space, Input, Upload, message, Modal, Tree } from 'antd';
import {
  FolderOutlined,
  FileOutlined,
  UploadOutlined,
  DownloadOutlined,
  DeleteOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
} from '@ant-design/icons';

const { Title } = Typography;
const { Search } = Input;

interface File {
  id: string;
  name: string;
  type: 'file' | 'folder';
  size: string;
  modified_at: string;
  path: string;
  permissions: string;
}

interface TreeNode {
  title: string;
  key: string;
  icon: React.ReactNode;
  children?: TreeNode[];
}

const FileManager: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [currentPath, setCurrentPath] = useState('/');
  const [fileContent, setFileContent] = useState('');
  const [contentModalVisible, setContentModalVisible] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [directoryTree, setDirectoryTree] = useState<TreeNode[]>([]);

  // 模拟数据
  const mockFiles: File[] = [
    {
      id: '1',
      name: 'Documents',
      type: 'folder',
      size: '0 B',
      modified_at: '2026-03-30 10:00:00',
      path: '/Documents',
      permissions: 'drwxr-xr-x',
    },
    {
      id: '2',
      name: 'Downloads',
      type: 'folder',
      size: '0 B',
      modified_at: '2026-03-30 10:00:00',
      path: '/Downloads',
      permissions: 'drwxr-xr-x',
    },
    {
      id: '3',
      name: 'script.ps1',
      type: 'file',
      size: '1.2 KB',
      modified_at: '2026-03-30 09:30:00',
      path: '/script.ps1',
      permissions: '-rw-r--r--',
    },
    {
      id: '4',
      name: 'config.txt',
      type: 'file',
      size: '512 B',
      modified_at: '2026-03-30 09:00:00',
      path: '/config.txt',
      permissions: '-rw-r--r--',
    },
  ];

  // 模拟目录树
  const mockDirectoryTree: TreeNode[] = [
    {
      title: '/',
      key: '/',
      icon: <FolderOutlined />,
      children: [
        {
          title: 'Documents',
          key: '/Documents',
          icon: <FolderOutlined />,
          children: [
            {
              title: 'report.docx',
              key: '/Documents/report.docx',
              icon: <FileTextOutlined />,
            },
          ],
        },
        {
          title: 'Downloads',
          key: '/Downloads',
          icon: <FolderOutlined />,
        },
        {
          title: 'script.ps1',
          key: '/script.ps1',
          icon: <FileOutlined />,
        },
        {
          title: 'config.txt',
          key: '/config.txt',
          icon: <FileOutlined />,
        },
      ],
    },
  ];

  React.useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setFiles(mockFiles);
      setDirectoryTree(mockDirectoryTree);
      setLoading(false);
    }, 1000);
  }, []);

  const handleFileUpload = (file: any) => {
    // 模拟文件上传
    setTimeout(() => {
      message.success('文件上传成功');
      const newFile: File = {
        id: (files.length + 1).toString(),
        name: file.name,
        type: 'file',
        size: '1.0 KB',
        modified_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
        path: `${currentPath}/${file.name}`,
        permissions: '-rw-r--r--',
      };
      setFiles([...files, newFile]);
    }, 1000);
    return false;
  };

  const handleFileDownload = (file: File) => {
    // 模拟文件下载
    message.success(`正在下载文件: ${file.name}`);
  };

  const handleDeleteFile = (id: string) => {
    setFiles(files.filter(file => file.id !== id));
    message.success('文件已删除');
  };

  const handleFileView = (file: File) => {
    setSelectedFile(file);
    // 模拟文件内容
    setFileContent(`This is the content of ${file.name}`);
    setContentModalVisible(true);
  };

  const handleDirectoryClick = (path: string) => {
    setCurrentPath(path);
    // 模拟切换目录
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 500);
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (name: string, record: File) => (
        <Space>
          {record.type === 'folder' ? <FolderOutlined /> : <FileOutlined />}
          <span>{name}</span>
        </Space>
      ),
    },
    {
      title: '大小',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: '修改时间',
      dataIndex: 'modified_at',
      key: 'modified_at',
    },
    {
      title: '权限',
      dataIndex: 'permissions',
      key: 'permissions',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: File) => (
        <Space size="middle">
          {record.type === 'file' && (
            <>
              <Button size="small" icon={<FileTextOutlined />} onClick={() => handleFileView(record)}>
                查看
              </Button>
              <Button size="small" icon={<DownloadOutlined />} onClick={() => handleFileDownload(record)}>
                下载
              </Button>
            </>
          )}
          {record.type === 'folder' && (
            <Button size="small" icon={<FolderOpenOutlined />} onClick={() => handleDirectoryClick(record.path)}>
              打开
            </Button>
          )}
          <Button danger size="small" icon={<DeleteOutlined />} onClick={() => handleDeleteFile(record.id)}>
            删除
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>文件管理</Title>
      
      <div style={{ display: 'flex', gap: 16, height: 'calc(100vh - 200px)' }}>
        <Card style={{ width: 300, flexShrink: 0 }} title="目录结构">
          <Tree
            treeData={directoryTree}
            defaultExpandAll
            onSelect={(selectedKeys) => {
              if (selectedKeys.length > 0) {
                handleDirectoryClick(selectedKeys[0] as string);
              }
            }}
          />
        </Card>
        
        <Card style={{ flex: 1 }} title={`当前路径: ${currentPath}`}>
          <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
            <Search placeholder="搜索文件" style={{ width: 300 }} />
            <Upload.Dragger name="file" customRequest={handleFileUpload} showUploadList={false}>
              <p className="ant-upload-drag-icon">
                <UploadOutlined />
              </p>
              <p className="ant-upload-text">点击或拖拽文件到此处上传</p>
              <p className="ant-upload-hint">
                支持单个文件上传
              </p>
            </Upload.Dragger>
          </div>
          
          {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
              <Spin size="large" />
            </div>
          ) : (
            <Table 
              columns={columns} 
              dataSource={files} 
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          )}
        </Card>
      </div>

      <Modal
        title={`查看文件: ${selectedFile?.name}`}
        open={contentModalVisible}
        onCancel={() => setContentModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setContentModalVisible(false)}>
            关闭
          </Button>,
        ]}
        width={800}
      >
        <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
          {fileContent}
        </pre>
      </Modal>
    </div>
  );
};

export default FileManager;