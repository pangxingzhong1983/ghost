import React, { useState, useEffect } from 'react';
import { Layout as AntLayout, Menu, Button, Dropdown, Space, Typography, Breadcrumb, Badge } from 'antd';
import {
  HomeOutlined, 
  UsergroupAddOutlined, 
  GlobalOutlined, 
  AppstoreAddOutlined, 
  ToolOutlined, 
  KeyOutlined, 
  OrderedListOutlined, 
  FolderOpenOutlined, 
  LineChartOutlined, 
  UserOutlined,
  SettingOutlined,
  TagOutlined,
  DashOutlined,
  CodeOutlined,
  LinkOutlined,
  CloudOutlined,
  FileTextOutlined,
  MonitorOutlined,
  DatabaseOutlined,
  FolderOutlined,
  PlayCircleOutlined,
  InfoCircleOutlined,
  DesktopOutlined,
  LogoutOutlined,
  ApiOutlined
} from '@ant-design/icons';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Layout.css';
import websocketService from '../services/websocket';

const { Header, Sider, Content } = AntLayout;
const { Title } = Typography;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [activeSessions, setActiveSessions] = useState(0);
  const [activeListeners, setActiveListeners] = useState(0);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const navigate = useNavigate();
  const location = useLocation();

  // 监听WebSocket连接状态和实时数据
  useEffect(() => {
    const checkConnectionStatus = () => {
      if (websocketService.isConnected()) {
        setConnectionStatus('connected');
        // 获取实时会话和监听器数量
        websocketService.getSessions().then(sessions => {
          setActiveSessions(sessions.length);
        }).catch(err => {
          console.error('Error getting sessions:', err);
          // WebSocket获取失败，使用默认值
          setActiveSessions(0);
        });

        websocketService.getListeners().then(listeners => {
          const activeCount = listeners.filter((l: any) => l.status === 'active').length;
          setActiveListeners(activeCount);
        }).catch(err => {
          console.error('Error getting listeners:', err);
          // WebSocket获取失败，使用默认值
          setActiveListeners(0);
        });
      } else {
        setConnectionStatus('disconnected');
        // WebSocket未连接，使用默认值
        setActiveSessions(0);
        setActiveListeners(0);
      }
    };

    checkConnectionStatus();
    const interval = setInterval(checkConnectionStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('tokenExpiry');
    localStorage.removeItem('user');
    websocketService.disconnect();
    navigate('/login');
  };

  const userMenu = [
    {
      key: 'profile',
      label: '个人资料',
    },
    {
      key: 'logout',
      label: (
        <a onClick={handleLogout}>
          <LogoutOutlined /> 登出
        </a>
      ),
    },
  ];

  // 面包屑导航配置
  const breadcrumbItems = [
    { title: <Link to="/dashboard">首页</Link> },
  ];

  // 根据当前路径添加面包屑
  const path = location.pathname;
  if (path === '/sessions') {
    breadcrumbItems.push({ title: <span>会话管理</span> });
  } else if (path === '/listeners') {
    breadcrumbItems.push({ title: <span>监听管理</span> });
  } else if (path === '/payloads') {
    breadcrumbItems.push({ title: <span>Payload生成</span> });
  } else if (path === '/modules') {
    breadcrumbItems.push({ title: <span>模块管理</span> });
  } else if (path === '/credentials') {
    breadcrumbItems.push({ title: <span>凭证管理</span> });
  } else if (path === '/jobs') {
    breadcrumbItems.push({ title: <span>作业管理</span> });
  } else if (path === '/file-manager') {
    breadcrumbItems.push({ title: <span>文件管理</span> });
  } else if (path === '/network') {
    breadcrumbItems.push({ title: <span>网络工具</span> });
  } else if (path === '/config') {
    breadcrumbItems.push({ title: <span>配置管理</span> });
  } else if (path === '/tags') {
    breadcrumbItems.push({ title: <span>标签管理</span> });
  } else if (path === '/dns-c2') {
    breadcrumbItems.push({ title: <span>DNS C2</span> });
  } else if (path === '/python') {
    breadcrumbItems.push({ title: <span>Python控制台</span> });
  } else if (path === '/connect') {
    breadcrumbItems.push({ title: <span>连接管理</span> });
  } else if (path === '/exposed') {
    breadcrumbItems.push({ title: <span>暴露服务</span> });
  } else if (path === '/logging') {
    breadcrumbItems.push({ title: <span>日志管理</span> });
  } else if (path === '/screen-control') {
    breadcrumbItems.push({ title: <span>屏幕控制</span> });
  } else if (path === '/keylogger') {
    breadcrumbItems.push({ title: <span>键盘记录</span> });
  } else if (path === '/system-info') {
    breadcrumbItems.push({ title: <span>系统信息</span> });
  } else if (path === '/process-manager') {
    breadcrumbItems.push({ title: <span>进程管理</span> });
  } else if (path === '/security-tools') {
    breadcrumbItems.push({ title: <span>安全工具</span> });
  } else if (path === '/network-tools') {
    breadcrumbItems.push({ title: <span>网络工具</span> });
  } else if (path === '/system-tools') {
    breadcrumbItems.push({ title: <span>系统工具</span> });
  } else if (path === '/data-collection') {
    breadcrumbItems.push({ title: <span>数据收集</span> });
  } else if (path === '/file-system') {
    breadcrumbItems.push({ title: <span>文件系统</span> });
  } else if (path === '/execution-tools') {
    breadcrumbItems.push({ title: <span>执行工具</span> });  } else if (path === '/utilities') {
    breadcrumbItems.push({ title: <span>综合工具</span> });
  } else if (path === '/dashboard') {
    breadcrumbItems.push({ title: <span>仪表盘</span> });
  }

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed} width={240}>
        <div className="logo" style={{ padding: '16px', textAlign: 'center' }}>
          <Title level={3} style={{ color: 'white', margin: 0 }}>
            {collapsed ? 'G' : 'Ghost C2'}
          </Title>
          <div style={{ color: '#888', fontSize: '12px', marginTop: '8px' }}>
            {collapsed ? '' : '跨平台C2工具'}
          </div>
        </div>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['dashboard']}>
          {/* 核心功能 */}
          <Menu.SubMenu key="core" title="核心功能" icon={<HomeOutlined />}>
            <Menu.Item key="dashboard" icon={<HomeOutlined />}>
              <Link to="/dashboard">仪表盘</Link>
            </Menu.Item>
            <Menu.Item key="sessions" icon={<UsergroupAddOutlined />}>
              <Space>
                <Link to="/sessions">会话管理</Link>
                <Badge count={activeSessions} size="small" style={{ backgroundColor: '#52c41a' }} />
              </Space>
            </Menu.Item>
            <Menu.Item key="listeners" icon={<GlobalOutlined />}>
              <Space>
                <Link to="/listeners">监听管理</Link>
                <Badge count={activeListeners} size="small" style={{ backgroundColor: '#1890ff' }} />
              </Space>
            </Menu.Item>
            <Menu.Item key="payloads" icon={<AppstoreAddOutlined />}>
              <Link to="/payloads">Payload生成</Link>
            </Menu.Item>
            <Menu.Item key="connect" icon={<LinkOutlined />}>
              <Link to="/connect">连接管理</Link>
            </Menu.Item>
          </Menu.SubMenu>

          {/* 资产管理 */}
          <Menu.SubMenu key="assets" title="资产管理" icon={<DatabaseOutlined />}>
            <Menu.Item key="modules" icon={<ToolOutlined />}>
              <Link to="/modules">模块管理</Link>
            </Menu.Item>
            <Menu.Item key="credentials" icon={<KeyOutlined />}>
              <Link to="/credentials">凭证管理</Link>
            </Menu.Item>
            <Menu.Item key="file-manager" icon={<FolderOpenOutlined />}>
              <Link to="/file-manager">文件管理</Link>
            </Menu.Item>
            <Menu.Item key="file-system" icon={<FolderOutlined />}>
              <Link to="/file-system">文件系统</Link>
            </Menu.Item>
          </Menu.SubMenu>

          {/* 任务管理 */}
          <Menu.SubMenu key="tasks" title="任务管理" icon={<OrderedListOutlined />}>
            <Menu.Item key="jobs" icon={<OrderedListOutlined />}>
              <Link to="/jobs">作业管理</Link>
            </Menu.Item>
            <Menu.Item key="tags" icon={<TagOutlined />}>
              <Link to="/tags">标签管理</Link>
            </Menu.Item>
          </Menu.SubMenu>

          {/* 监控与控制 */}
          <Menu.SubMenu key="monitoring" title="监控与控制" icon={<MonitorOutlined />}>
            <Menu.Item key="screen-control" icon={<MonitorOutlined />}>
              <Link to="/screen-control">屏幕控制</Link>
            </Menu.Item>
            <Menu.Item key="keylogger" icon={<KeyOutlined />}>
              <Link to="/keylogger">键盘记录</Link>
            </Menu.Item>
            <Menu.Item key="system-info" icon={<InfoCircleOutlined />}>
              <Link to="/system-info">系统信息</Link>
            </Menu.Item>
            <Menu.Item key="process-manager" icon={<DesktopOutlined />}>
              <Link to="/process-manager">进程管理</Link>
            </Menu.Item>
          </Menu.SubMenu>

          {/* 系统工具 */}
          <Menu.SubMenu key="system" title="系统工具" icon={<SettingOutlined />}>
            <Menu.Item key="network" icon={<LineChartOutlined />}>
              <Link to="/network">网络工具</Link>
            </Menu.Item>
            <Menu.Item key="system-tools" icon={<SettingOutlined />}>
              <Link to="/system-tools">系统工具</Link>
            </Menu.Item>
            <Menu.Item key="security-tools" icon={<ApiOutlined />}>
              <Link to="/security-tools">安全工具</Link>
            </Menu.Item>
            <Menu.Item key="execution-tools" icon={<PlayCircleOutlined />}>
              <Link to="/execution-tools">执行工具</Link>
            </Menu.Item>
            <Menu.Item key="data-collection" icon={<DatabaseOutlined />}>
              <Link to="/data-collection">数据收集</Link>
            </Menu.Item>
            <Menu.Item key="utilities" icon={<ToolOutlined />}>
              <Link to="/utilities">综合工具</Link>
            </Menu.Item>
          </Menu.SubMenu>

          {/* 高级功能 */}
          <Menu.SubMenu key="advanced" title="高级功能" icon={<CodeOutlined />}>
            <Menu.Item key="dns-c2" icon={<DashOutlined />}>
              <Link to="/dns-c2">DNS C2</Link>
            </Menu.Item>
            <Menu.Item key="python" icon={<CodeOutlined />}>
              <Link to="/python">Python控制台</Link>
            </Menu.Item>
            <Menu.Item key="exposed" icon={<CloudOutlined />}>
              <Link to="/exposed">暴露服务</Link>
            </Menu.Item>
            <Menu.Item key="logging" icon={<FileTextOutlined />}>
              <Link to="/logging">日志管理</Link>
            </Menu.Item>
            <Menu.Item key="config" icon={<SettingOutlined />}>
              <Link to="/config">配置管理</Link>
            </Menu.Item>
          </Menu.SubMenu>
        </Menu>
      </Sider>
      <AntLayout className="site-layout">
        <Header className="site-layout-background" style={{ padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Breadcrumb items={breadcrumbItems} />
          </div>
          <Space>
            <Badge status={connectionStatus === 'connected' ? 'success' : 'error'} text={connectionStatus === 'connected' ? '已连接' : '未连接'} />
            <Dropdown menu={{ items: userMenu }}>
              <Button type="text" icon={<UserOutlined />} style={{ color: 'white' }}>
                {localStorage.getItem('user') || '管理员'}
              </Button>
            </Dropdown>
          </Space>
        </Header>
        <Content
          className="site-layout-background"
          style={{
            margin: '24px 16px',
            padding: 24,
            minHeight: 280,
            borderRadius: 8,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.09)',
          }}
        >
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;