import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Typography, Tag, Modal, message, Spin, Progress } from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  DeleteOutlined,
} from '@ant-design/icons';

const { Title } = Typography;

interface Job {
  id: string;
  name: string;
  type: string;
  status: 'running' | 'pending' | 'completed' | 'failed' | 'stopped';
  progress: number;
  started_at: string;
  completed_at: string | null;
  target: string;
  command: string;
}

const Jobs: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  // 模拟数据
  const mockJobs: Job[] = [
    {
      id: '1',
      name: 'Mimikatz 执行',
      type: 'command',
      status: 'running',
      progress: 75,
      started_at: '2026-03-30 14:30:00',
      completed_at: null,
      target: 'Session #1',
      command: 'mimikatz',
    },
    {
      id: '2',
      name: '系统信息收集',
      type: 'module',
      status: 'completed',
      progress: 100,
      started_at: '2026-03-30 14:20:00',
      completed_at: '2026-03-30 14:25:00',
      target: 'Session #1',
      command: 'sysinfo',
    },
    {
      id: '3',
      name: '文件上传',
      type: 'upload',
      status: 'pending',
      progress: 0,
      started_at: '2026-03-30 14:15:00',
      completed_at: null,
      target: 'Session #2',
      command: 'upload file.txt C:/temp/',
    },
    {
      id: '4',
      name: '端口扫描',
      type: 'scan',
      status: 'failed',
      progress: 0,
      started_at: '2026-03-30 14:10:00',
      completed_at: '2026-03-30 14:12:00',
      target: '192.168.1.0/24',
      command: 'portscan',
    },
  ];

  useEffect(() => {
    // 模拟加载数据
    setTimeout(() => {
      setJobs(mockJobs);
      setLoading(false);
    }, 1000);
  }, []);

  const handleJobStart = (id: string) => {
    setJobs(jobs.map(job => 
      job.id === id ? { ...job, status: 'running', progress: 0 } : job
    ));
    message.success('作业已开始');
  };

  const handleJobPause = (id: string) => {
    setJobs(jobs.map(job => 
      job.id === id ? { ...job, status: 'stopped' } : job
    ));
    message.success('作业已暂停');
  };

  const handleJobDelete = (id: string) => {
    setJobs(jobs.filter(job => job.id !== id));
    message.success('作业已删除');
  };

  const handleJobDetail = (job: Job) => {
    setSelectedJob(job);
    setDetailModalVisible(true);
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={type === 'command' ? 'blue' : type === 'module' ? 'green' : type === 'upload' ? 'purple' : 'orange'}>
          {type}
        </Tag>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = '';
        let text = '';
        switch (status) {
          case 'running':
            color = 'green';
            text = '运行中';
            break;
          case 'pending':
            color = 'orange';
            text = '等待中';
            break;
          case 'completed':
            color = 'blue';
            text = '已完成';
            break;
          case 'failed':
            color = 'red';
            text = '失败';
            break;
          case 'stopped':
            color = 'gray';
            text = '已停止';
            break;
          default:
            color = 'default';
            text = status;
        }
        return <Tag color={color}>{text}</Tag>;
      },
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress: number) => (
        <Progress percent={progress} size="small" />
      ),
    },
    {
      title: '目标',
      dataIndex: 'target',
      key: 'target',
    },
    {
      title: '开始时间',
      dataIndex: 'started_at',
      key: 'started_at',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Job) => (
        <Space size="middle">
          {record.status === 'pending' && (
            <Button type="primary" size="small" onClick={() => handleJobStart(record.id)}>
              <PlayCircleOutlined />
            </Button>
          )}
          {record.status === 'running' && (
            <Button size="small" onClick={() => handleJobPause(record.id)}>
              <PauseCircleOutlined />
            </Button>
          )}
          <Button size="small" onClick={() => handleJobDetail(record)}>
            详情
          </Button>
          <Button danger size="small" onClick={() => handleJobDelete(record.id)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>作业管理</Title>
      
      <Card>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <Spin size="large" />
          </div>
        ) : (
          <Table 
            columns={columns} 
            dataSource={jobs} 
            rowKey="id"
            pagination={{ pageSize: 10 }}
          />
        )}
      </Card>

      <Modal
        title="作业详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>,
        ]}
        width={600}
      >
        {selectedJob && (
          <div>
            <p><strong>名称:</strong> {selectedJob.name}</p>
            <p><strong>类型:</strong> {selectedJob.type}</p>
            <p><strong>状态:</strong> {selectedJob.status}</p>
            <p><strong>目标:</strong> {selectedJob.target}</p>
            <p><strong>命令:</strong> {selectedJob.command}</p>
            <p><strong>开始时间:</strong> {selectedJob.started_at}</p>
            {selectedJob.completed_at && (
              <p><strong>完成时间:</strong> {selectedJob.completed_at}</p>
            )}
            <p><strong>进度:</strong> {selectedJob.progress}%</p>
            <div style={{ marginTop: 20 }}>
              <Title level={5}>输出</Title>
              <pre style={{ backgroundColor: '#f5f5f5', padding: 10, borderRadius: 4 }}>
                模拟作业输出...
              </pre>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Jobs;