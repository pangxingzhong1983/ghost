import React, { useState, useRef, useEffect } from 'react';
import { Card, Typography, Input, Button, Space, List, Spin } from 'antd';
import { SendOutlined, ClearOutlined, CodeOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

const PythonConsole: React.FC = () => {
  const [commands, setCommands] = useState<{id: string, command: string, output: string, timestamp: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);

  const executeCommand = (command: string) => {
    if (!command.trim()) return;

    setLoading(true);
    
    // 模拟Python命令执行
    setTimeout(() => {
      const output = simulatePythonExecution(command);
      const newCommand = {
        id: Date.now().toString(),
        command,
        output,
        timestamp: new Date().toISOString().slice(0, 19).replace('T', ' '),
      };
      setCommands([...commands, newCommand]);
      setInput('');
      setLoading(false);
    }, 1000);
  };

  const simulatePythonExecution = (command: string): string => {
    // 模拟Python命令执行结果
    if (command.includes('import os')) {
      return '>>> import os\n>>> ';
    } else if (command.includes('os.system')) {
      return '>>> os.system("whoami")\nadmin\n0\n>>> ';
    } else if (command.includes('print(')) {
      const message = command.match(/print\((.*?)\)/)?.[1] || '';
      return `>>> ${command}\n${message.replace(/['"]/g, '')}\n>>> `;
    } else if (command.includes('sessions')) {
      return '>>> sessions\n[1] Session #1 (Windows 10, 192.168.1.100)\n[2] Session #2 (Linux, 192.168.1.101)\n>>> ';
    } else if (command.includes('listeners')) {
      return '>>> listeners\n[1] HTTP Listener (192.168.1.100:8080)\n[2] TCP Listener (192.168.1.100:4444)\n>>> ';
    } else {
      return `>>> ${command}\n${command}\n>>> `;
    }
  };

  const clearConsole = () => {
    setCommands([]);
  };

  useEffect(() => {
    // 自动滚动到底部
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [commands]);

  return (
    <div>
      <Title level={2}>Python控制台</Title>
      
      <Card>
        <div style={{ marginBottom: 16 }}>
          <Text type="secondary">在下方输入Python命令，支持执行Ghost内置命令和Python代码</Text>
        </div>
        
        <div 
          ref={listRef}
          style={{ 
            height: 400, 
            border: '1px solid #f0f0f0', 
            borderRadius: 4, 
            padding: 16, 
            overflowY: 'auto',
            backgroundColor: '#fafafa',
            fontFamily: 'monospace'
          }}
        >
          <List
            dataSource={commands}
            renderItem={(item) => (
              <List.Item>
                <div style={{ marginBottom: 8 }}>
                  <Text type="secondary">{item.timestamp}</Text>
                </div>
                <div style={{ marginBottom: 4 }}>
                  <Text style={{ color: '#d73a49' }}>&gt;&gt;&gt;&gt; {item.command}</Text>
                </div>
                <div style={{ whiteSpace: 'pre-wrap' }}>
                  <Text>{item.output}</Text>
                </div>
              </List.Item>
            )}
          />
          {loading && (
            <div style={{ display: 'flex', justifyContent: 'center', padding: 16 }}>
              <Spin size="small" />
            </div>
          )}
        </div>
        
        <div style={{ marginTop: 16, display: 'flex' }}>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onPressEnter={() => executeCommand(input)}
            placeholder="输入Python命令..."
            style={{ flex: 1, marginRight: 8 }}
          />
          <Space>
            <Button 
              type="primary" 
              icon={<SendOutlined />} 
              onClick={() => executeCommand(input)}
              loading={loading}
            >
              执行
            </Button>
            <Button 
              icon={<ClearOutlined />} 
              onClick={clearConsole}
            >
              清空
            </Button>
          </Space>
        </div>
        
        <div style={{ marginTop: 16 }}>
          <Title level={5}>常用命令示例</Title>
          <Space direction="vertical" size={8}>
            <Button 
              type="text" 
              icon={<CodeOutlined />} 
              onClick={() => setInput('sessions')}
            >
              sessions - 查看所有会话
            </Button>
            <Button 
              type="text" 
              icon={<CodeOutlined />} 
              onClick={() => setInput('listeners')}
            >
              listeners - 查看所有监听器
            </Button>
            <Button 
              type="text" 
              icon={<CodeOutlined />} 
              onClick={() => setInput('import os; os.system("whoami")')}
            >
              import os; os.system("whoami") - 执行系统命令
            </Button>
            <Button 
              type="text" 
              icon={<CodeOutlined />} 
              onClick={() => setInput('print("Hello Ghost!")')}
            >
              print("Hello Ghost!") - 打印消息
            </Button>
          </Space>
        </div>
      </Card>
    </div>
  );
};

export default PythonConsole;