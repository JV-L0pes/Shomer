// frontend/src/components/AuthPage.tsx
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Eye,
  EyeOff,
  User,
  Mail,
  Lock,
  ArrowRight,
  Shield,
  Camera,
} from "lucide-react";

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface FormErrors {
  username?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  general?: string;
}

interface User {
  id: string;
  username: string;
  email: string;
  createdAt: string;
}

interface AuthPageProps {
  onLogin: (user: User) => void;
}

// Dados de teste - credenciais válidas
const TEST_USERS = [
  {
    id: "1",
    username: "admin",
    email: "admin@shomer.com",
    password: "Shomer123",
    createdAt: "2025-01-15T10:00:00Z",
  },
  {
    id: "2",
    username: "demo",
    email: "demo@shomer.com",
    password: "Demo123",
    createdAt: "2025-01-15T10:30:00Z",
  },
  {
    id: "3",
    username: "test",
    email: "test@shomer.com",
    password: "Test123",
    createdAt: "2025-01-15T11:00:00Z",
  },
];

export default function AuthPage({ onLogin }: AuthPageProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});

  const validateField = (field: keyof FormData, value: string): string => {
    switch (field) {
      case "username":
        if (!value) return "Nome de usuário é obrigatório";
        if (value.length < 3) return "Mínimo 3 caracteres";
        return "";

      case "email":
        if (!value) return "Email é obrigatório";
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Email inválido";
        return "";

      case "password":
        if (!value) return "Senha é obrigatória";
        if (value.length < 6) return "Mínimo 6 caracteres";
        return "";

      case "confirmPassword":
        if (!isLogin && value !== formData.password)
          return "Senhas não coincidem";
        return "";

      default:
        return "";
    }
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    const error = validateField(field, value);
    setErrors((prev) => ({ ...prev, [field]: error }));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (isLogin) {
      newErrors.username = validateField("username", formData.username);
      newErrors.password = validateField("password", formData.password);
    } else {
      newErrors.username = validateField("username", formData.username);
      newErrors.email = validateField("email", formData.email);
      newErrors.password = validateField("password", formData.password);
      newErrors.confirmPassword = validateField(
        "confirmPassword",
        formData.confirmPassword
      );
    }

    Object.keys(newErrors).forEach((key) => {
      if (!newErrors[key as keyof FormErrors]) {
        delete newErrors[key as keyof FormErrors];
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    setErrors({});

    try {
      await new Promise((resolve) => setTimeout(resolve, 1500));

      if (isLogin) {
        const user = TEST_USERS.find(
          (u) =>
            u.username === formData.username && u.password === formData.password
        );

        if (user) {
          onLogin({
            id: user.id,
            username: user.username,
            email: user.email,
            createdAt: user.createdAt,
          });
        } else {
          setErrors({
            general:
              "Credenciais inválidas. Use: admin/Shomer123, demo/Demo123 ou test/Test123",
          });
        }
      } else {
        // Simular registro bem-sucedido
        const newUser: User = {
          id: String(Date.now()),
          username: formData.username,
          email: formData.email,
          createdAt: new Date().toISOString(),
        };

        alert("Registro realizado! Agora faça login.");
        setIsLogin(true);
        setFormData({
          username: formData.username,
          email: "",
          password: "",
          confirmPassword: "",
        });
      }
    } catch (error) {
      setErrors({ general: "Erro interno. Tente novamente." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-[#020617] to-[#0f172a] flex items-center justify-center p-4">
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 via-blue-500/20 to-purple-500/20 animate-pulse" />
      </div>

      <div className="relative z-10 w-full max-w-md">
        {/* Header */}
        <motion.div
          className="text-center mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl">
              <Camera className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-cyan-400 tracking-wide">
              Shomer
            </h1>
          </div>
          <p className="text-gray-400 text-sm">
            Sistema de Monitoramento Inteligente
          </p>
        </motion.div>

        {/* Auth Card */}
        <motion.div
          className="bg-gray-900/80 backdrop-blur-xl border border-gray-700/50 rounded-2xl shadow-2xl p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          {/* Credenciais de Teste */}
          <motion.div
            className="mb-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-xl"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <h3 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
              <Shield className="w-4 h-4" />
              Credenciais de Teste
            </h3>
            <div className="text-xs text-blue-300 space-y-1">
              <div>
                <span className="font-mono">admin</span> /{" "}
                <span className="font-mono">Shomer123</span>
              </div>
              <div>
                <span className="font-mono">demo</span> /{" "}
                <span className="font-mono">Demo123</span>
              </div>
              <div>
                <span className="font-mono">test</span> /{" "}
                <span className="font-mono">Test123</span>
              </div>
            </div>
          </motion.div>

          {/* Tabs */}
          <div className="flex mb-8 bg-gray-800/50 rounded-xl p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-medium ${
                isLogin
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              <Shield className="w-4 h-4" />
              Entrar
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-medium ${
                !isLogin
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-gray-400 hover:text-gray-200"
              }`}
            >
              <User className="w-4 h-4" />
              Registrar
            </button>
          </div>

          {/* Form Fields */}
          <div className="space-y-5">
            {/* Username */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Nome de Usuário
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) =>
                    handleInputChange("username", e.target.value)
                  }
                  className={`w-full pl-12 pr-4 py-3 bg-gray-800/50 border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 text-white placeholder-gray-500 ${
                    errors.username
                      ? "border-red-500/50 focus:ring-red-500/50"
                      : "border-gray-600/50 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                  }`}
                  placeholder="Seu nome de usuário"
                />
              </div>
              {errors.username && (
                <motion.p
                  className="text-red-400 text-sm mt-1"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  ⚠️ {errors.username}
                </motion.p>
              )}
            </div>

            {/* Email (registro apenas) */}
            <AnimatePresence>
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) =>
                        handleInputChange("email", e.target.value)
                      }
                      className={`w-full pl-12 pr-4 py-3 bg-gray-800/50 border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 text-white placeholder-gray-500 ${
                        errors.email
                          ? "border-red-500/50 focus:ring-red-500/50"
                          : "border-gray-600/50 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                      }`}
                      placeholder="seu@email.com"
                    />
                  </div>
                  {errors.email && (
                    <motion.p
                      className="text-red-400 text-sm mt-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      ⚠️ {errors.email}
                    </motion.p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(e) =>
                    handleInputChange("password", e.target.value)
                  }
                  className={`w-full pl-12 pr-12 py-3 bg-gray-800/50 border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 text-white placeholder-gray-500 ${
                    errors.password
                      ? "border-red-500/50 focus:ring-red-500/50"
                      : "border-gray-600/50 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                  }`}
                  placeholder="Sua senha"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-200 transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
              {errors.password && (
                <motion.p
                  className="text-red-400 text-sm mt-1"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  ⚠️ {errors.password}
                </motion.p>
              )}
            </div>

            {/* Confirm Password (registro apenas) */}
            <AnimatePresence>
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Confirmar Senha
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      value={formData.confirmPassword}
                      onChange={(e) =>
                        handleInputChange("confirmPassword", e.target.value)
                      }
                      className={`w-full pl-12 pr-12 py-3 bg-gray-800/50 border rounded-xl focus:outline-none focus:ring-2 transition-all duration-300 text-white placeholder-gray-500 ${
                        errors.confirmPassword
                          ? "border-red-500/50 focus:ring-red-500/50"
                          : "border-gray-600/50 focus:ring-cyan-500/50 focus:border-cyan-500/50"
                      }`}
                      placeholder="Confirme sua senha"
                    />
                    <button
                      type="button"
                      onClick={() =>
                        setShowConfirmPassword(!showConfirmPassword)
                      }
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-200 transition-colors"
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  {errors.confirmPassword && (
                    <motion.p
                      className="text-red-400 text-sm mt-1"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      ⚠️ {errors.confirmPassword}
                    </motion.p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Erro Geral */}
            {errors.general && (
              <motion.div
                className="p-4 bg-red-500/20 border border-red-500/30 rounded-xl"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <p className="text-red-300 text-sm text-center">
                  {errors.general}
                </p>
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              onClick={handleSubmit}
              disabled={isLoading}
              className={`w-full group relative px-6 py-4 rounded-xl font-semibold text-white transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center justify-center gap-3 ${
                isLoading
                  ? "bg-gray-600 animate-pulse"
                  : "bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 shadow-lg hover:shadow-xl"
              }`}
              whileHover={!isLoading ? { y: -2 } : {}}
              whileTap={!isLoading ? { scale: 0.98 } : {}}
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Processando...</span>
                </>
              ) : (
                <>
                  <span>{isLogin ? "Entrar" : "Criar Conta"}</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </motion.button>
          </div>

          {/* Toggle Mode */}
          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              {isLogin ? "Não tem uma conta?" : "Já tem uma conta?"}{" "}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors hover:underline"
              >
                {isLogin ? "Registre-se aqui" : "Faça login aqui"}
              </button>
            </p>
          </div>
        </motion.div>

        {/* Footer */}
        <motion.div
          className="text-center mt-6 text-gray-500 text-xs"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <p>© 2025 Shomer - Sistema de Monitoramento Inteligente</p>
        </motion.div>
      </div>
    </div>
  );
}