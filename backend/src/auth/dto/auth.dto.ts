export interface RegisterDto {
  email: string;
  password: string;
  username?: string;
}

export interface LoginDto {
  email: string;
  password: string;
}

export interface AuthResponseDto {
  user: {
    id: string;
    email: string;
    username: string | null;
    membership: string;
    apiKey: string;
  };
  tokens: {
    accessToken: string;
    refreshToken: string;
  };
}
