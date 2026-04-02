import { message } from 'antd';

class WebSocketService {
  private socket: WebSocket | null = null;
  private listeners: Map<string, Array<(data: any) => void>> = new Map();
  private connected: boolean = false;
  private token: string | null = null;
  private cache: Map<string, { data: any; timestamp: number }> = new Map();
  private cacheExpiry = 5000; // 缓存过期时间（毫秒）

  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private url: string = 'ws://ghost.zhuquejiasu.uk/ws';

  connect(url: string = 'ws://ghost.zhuquejiasu.uk/ws'): Promise<void> {
    return new Promise((resolve, reject) => {
      // 如果已经有连接并且是打开状态，直接返回
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        console.log('WebSocket already connected');
        resolve();
        return;
      }

      // 如果正在连接中，等待连接完成
      if (this.socket && this.socket.readyState === WebSocket.CONNECTING) {
        console.log('WebSocket is connecting...');
        // 等待连接完成
        const checkConnection = setInterval(() => {
          if (this.socket?.readyState === WebSocket.OPEN) {
            clearInterval(checkConnection);
            resolve();
          } else if (this.socket?.readyState === WebSocket.CLOSED) {
            clearInterval(checkConnection);
            this.attemptReconnect(url, resolve, reject);
          }
        }, 100);
        return;
      }

      this.url = url;
      this.attemptReconnect(url, resolve, reject);
    });
  }

  private attemptReconnect(url: string, resolve: (value: void | PromiseLike<void>) => void, reject: (reason?: any) => void) {
    try {
      console.log(`Attempting to connect to WebSocket (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`);
      this.socket = new WebSocket(url);

      this.socket.onopen = () => {
        console.log('WebSocket connected');
        this.connected = true;
        this.reconnectAttempts = 0;
        // 只在首次连接时显示成功消息
        if (this.reconnectAttempts === 0) {
          message.success('WebSocket connected');
        }
        resolve();
      };

      this.socket.onclose = (event) => {
        console.log('WebSocket disconnected:', event.reason);
        this.connected = false;
        // 只在用户主动关闭时显示断开消息
        if (event.code !== 1000) {
          message.warning('WebSocket disconnected, attempting to reconnect...');
          this.scheduleReconnect();
        }
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        // 只在首次连接失败时显示错误消息
        if (this.reconnectAttempts === 0) {
          message.error('WebSocket error');
          reject(error);
        }
      };

      this.socket.onmessage = (event) => {
        try {
          console.log('Received WebSocket message:', event.data);
          const data = JSON.parse(event.data);
          console.log('Parsed WebSocket message:', data);
          if (data.event) {
            console.log('Processing event:', data.event);
            if (this.listeners.has(data.event)) {
              const eventListeners = this.listeners.get(data.event);
              console.log('Found listeners for event:', data.event, eventListeners?.length);
              eventListeners?.forEach(listener => listener(data.data));
            } else {
              console.log('No listeners for event:', data.event);
            }
          } else {
            console.log('No event in message:', data);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          console.error('Raw message:', event.data);
        }
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      if (this.reconnectAttempts === 0) {
        message.error('Failed to connect to WebSocket server');
        reject(error);
      } else {
        this.scheduleReconnect();
      }
    }
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
      console.log(`Scheduling reconnect in ${delay}ms`);
      setTimeout(() => {
        this.connect(this.url).catch(err => {
          console.error('Reconnect failed:', err);
        });
      }, delay);
    } else {
      console.error('Max reconnect attempts reached');
      message.error('Failed to reconnect to WebSocket server');
    }
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.close(1000, 'User disconnected');
      this.socket = null;
      this.connected = false;
      this.reconnectAttempts = 0;
    }
  }

  emit(event: string, data: any): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify({ event, data }));
    } else {
      console.error('WebSocket not connected');
      message.error('WebSocket not connected');
    }
  }

  on(event: string, callback: (data: any) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)?.push(callback);
  }

  off(event: string, callback: (data: any) => void): void {
    if (this.listeners.has(event)) {
      const eventListeners = this.listeners.get(event);
      if (eventListeners) {
        const index = eventListeners.indexOf(callback);
        if (index > -1) {
          eventListeners.splice(index, 1);
        }
      }
    }
  }

  // 认证
  authenticate(username: string, password: string): Promise<string> {
    return new Promise((resolve, reject) => {
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
        reject(new Error('WebSocket not connected'));
        return;
      }

      // 密码强度检查
      if (password.length < 6) {
        reject(new Error('Password must be at least 6 characters'));
        return;
      }

      const authId = Date.now().toString();

      // 监听认证结果
      const handleAuthResponse = (data: any) => {
        if (data.id === authId) {
          this.off('auth_response', handleAuthResponse);
          if (data.success) {
            this.token = data.token;
            // 使用localStorage存储令牌，并设置过期时间
            const expiry = new Date();
            expiry.setHours(expiry.getHours() + 24); // 24小时过期
            localStorage.setItem('token', data.token);
            localStorage.setItem('tokenExpiry', expiry.toISOString());
            message.success('Authentication successful');
            resolve(data.token);
          } else {
            message.error('Authentication failed');
            reject(new Error(data.error || 'Authentication failed'));
          }
        }
      };

      this.on('auth_response', handleAuthResponse);

      // 发送认证请求
      this.emit('auth', {
        id: authId,
        username,
        password,
      });
    });
  }

  // 执行Ghost命令
  executeCommand(command: string, args: string[] = []): Promise<any> {
    // 生成缓存键
    const cacheKey = `${command}:${args.join(':')}`;
    
    // 检查缓存
    const cachedData = this.cache.get(cacheKey);
    const now = Date.now();
    if (cachedData && (now - cachedData.timestamp) < this.cacheExpiry) {
      console.log('Using cached data for command:', cacheKey);
      return Promise.resolve(cachedData.data);
    }

    return new Promise((resolve, reject) => {
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
        console.error('WebSocket not connected');
        reject(new Error('WebSocket not connected'));
        return;
      }

      const commandId = Date.now().toString();
      console.log('Sending command:', command, args, 'with id:', commandId);

      // 监听命令执行结果
      const handleResponse = (data: any) => {
        console.log('Received response for command:', command, 'with data:', data);
        if (data.id === commandId) {
          console.log('Response matches command id:', commandId);
          this.off('command_response', handleResponse);
          if (data.error) {
            console.error('Command failed:', data.error);
            message.error(`Command failed: ${data.error}`);
            reject(new Error(data.error));
          } else {
            console.log('Command succeeded with result:', data.result);
            // 缓存结果
            this.cache.set(cacheKey, {
              data: data.result,
              timestamp: now
            });
            resolve(data.result);
          }
        } else {
          console.log('Response id does not match command id:', data.id, '!==', commandId);
        }
      };

      this.on('command_response', handleResponse);

      // 发送命令
      this.emit('command', {
        id: commandId,
        command,
        args,
      });
    });
  }

  // 获取会话列表
  getSessions(): Promise<any> {
    return this.executeCommand('sessions');
  }

  // 获取监听器列表
  getListeners(): Promise<any> {
    return this.executeCommand('listen', ['--list']);
  }

  // 生成Payload
  generatePayload(options: any): Promise<any> {
    const args = [];
    if (options.platform) args.push('--platform', options.platform);
    if (options.arch) args.push('--arch', options.arch);
    if (options.format) args.push('--format', options.format);
    if (options.transport) args.push('--transport', options.transport);
    if (options.host) args.push('--host', options.host);
    if (options.port) args.push('--port', options.port);
    if (options.output) args.push('--output', options.output);
    return this.executeCommand('gen', args);
  }

  // 添加监听器
  addListener(transport: string, args: string[]): Promise<any> {
    return this.executeCommand('listen', ['--add', transport, ...args]);
  }

  // 移除监听器
  removeListener(transport: string): Promise<any> {
    return this.executeCommand('listen', ['--remove', transport]);
  }

  // 获取凭证列表
  getCredentials(): Promise<any> {
    return this.executeCommand('creds');
  }

  // 获取作业列表
  getJobs(): Promise<any> {
    return this.executeCommand('job', ['list']);
  }

  // 获取Payload列表
  getPayloads(): Promise<any> {
    return this.executeCommand('payload', ['list']);
  }

  // 终止作业
  killJob(jobId: string): Promise<any> {
    return this.executeCommand('jobs', ['--kill', jobId]);
  }

  // 获取DNS C2状态
  getDnsC2Status(): Promise<any> {
    return this.executeCommand('dnscnc', ['status']);
  }

  // 获取DNS C2会话
  getDnsC2Sessions(): Promise<any> {
    return this.executeCommand('dnscnc', ['sessions']);
  }

  // 执行Python代码
  executePython(code: string): Promise<any> {
    return this.executeCommand('python', [code]);
  }

  // 获取配置
  getConfig(section?: string): Promise<any> {
    if (section) {
      return this.executeCommand('config', ['list', section]);
    }
    return this.executeCommand('config', ['list']);
  }

  // 设置配置
  setConfig(section: string, key: string, value: string): Promise<any> {
    return this.executeCommand('config', ['set', section, key, value]);
  }

  // 添加标签
  addTag(_node: string, tags: string[]): Promise<any> {
    return this.executeCommand('tag', ['--add', ...tags]);
  }

  // 移除标签
  removeTag(_node: string, tags: string[]): Promise<any> {
    return this.executeCommand('tag', ['--remove', ...tags]);
  }

  isConnected(): boolean {
    return this.connected;
  }

  getToken(): string | null {
    return this.token;
  }

  setToken(token: string): void {
    this.token = token;
  }

  // 检查令牌是否过期
  isTokenExpired(): boolean {
    const expiryStr = localStorage.getItem('tokenExpiry');
    if (!expiryStr) {
      return true;
    }
    const expiry = new Date(expiryStr);
    return new Date() > expiry;
  }

  // 验证令牌有效性
  validateToken(): boolean {
    const token = localStorage.getItem('token');
    if (!token) {
      return false;
    }
    if (this.isTokenExpired()) {
      localStorage.removeItem('token');
      localStorage.removeItem('tokenExpiry');
      this.token = null;
      return false;
    }
    return true;
  }

  // 清除缓存
  clearCache(): void {
    this.cache.clear();
    console.log('Cache cleared');
  }

  // 清除特定命令的缓存
  clearCacheForCommand(command: string, args: string[] = []): void {
    const cacheKey = `${command}:${args.join(':')}`;
    this.cache.delete(cacheKey);
    console.log('Cache cleared for command:', cacheKey);
  }
}

export default new WebSocketService();