import { useState } from "react";
import { useNavigate } from "react-router-dom";

interface AuthResponse {
  msg: string;
  token?: string;
}

export default function AuthPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [invitationToken, setInvitationToken] = useState("");
  const [isRegisterMode, setIsRegisterMode] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const apiUrl = import.meta.env.VITE_API_URL;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const endpoint = isRegisterMode ? "/register" : "/login";
    const payload: any = { username, password };
    if (isRegisterMode) payload.invitationToken = invitationToken;

    try {
      const res = await fetch(`${apiUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || data.msg || "Erro na requisição");
      }
      const data: AuthResponse = await res.json();
      if (!isRegisterMode && data.token) {
        localStorage.setItem("authToken", data.token);
      }
      navigate("/demo");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      <div className="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-white mb-6">
          {isRegisterMode ? "Registro" : "Login"}
        </h2>

        {error && (
          <div className="mb-4 p-2 bg-red-700 text-red-200 rounded">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-gray-300 mb-1">Usuário</label>
            <input
              type="text"
              className="w-full px-4 py-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-gray-300 mb-1">Senha</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {isRegisterMode && (
            <div>
              <label className="block text-gray-300 mb-1">Token de Convite</label>
              <input
                type="text"
                className="w-full px-4 py-2 rounded bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={invitationToken}
                onChange={(e) => setInvitationToken(e.target.value)}
                required
              />
            </div>
          )}

          <button
            type="submit"
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded transition"
          >
            {isRegisterMode ? "Registrar" : "Entrar"}
          </button>
        </form>

        <div className="mt-6 text-center text-gray-400">
          {isRegisterMode ? "Já tem conta?" : "Não tem conta?"}{" "}
          <button
            onClick={() => setIsRegisterMode(!isRegisterMode)}
            className="text-blue-400 hover:underline"
          >
            {isRegisterMode ? "Faça login" : "Registre-se"}
          </button>
        </div>
      </div>
    </div>
  );
}
