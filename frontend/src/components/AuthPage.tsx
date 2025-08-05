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
import { useNavigate } from "react-router-dom";
import { loginApi, registerApi } from "../api";

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  invitationToken: string;
}

interface FormErrors {
  username?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  invitationToken?: string;
  general?: string;
}

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    invitationToken: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const navigate = useNavigate();

  const validateField = (field: keyof FormData, value: string): string => {
    switch (field) {
      case "username":
        if (!value.trim()) return "Nome de usuário é obrigatório";
        if (value.length < 3)
          return "Nome de usuário deve ter pelo menos 3 caracteres";
        if (value.length > 20)
          return "Nome de usuário deve ter no máximo 20 caracteres";
        return "";

      case "email":
        if (!isLogin && !value.trim()) return "Email é obrigatório";
        if (!isLogin && value.trim()) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(value)) return "Email inválido";
        }
        return "";

      case "password":
        if (!value.trim()) return "Senha é obrigatória";
        if (value.length < 6) return "Senha deve ter pelo menos 6 caracteres";
        return "";

      case "confirmPassword":
        if (!isLogin && !value.trim()) return "Confirme sua senha";
        if (!isLogin && value !== formData.password)
          return "Senhas não coincidem";
        return "";

      case "invitationToken":
        if (!isLogin && !value.trim()) return "Token de convite é obrigatório";
        return "";

      default:
        return "";
    }
  };

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setErrors((prev) => ({ ...prev, [field]: validateField(field, value) }));
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Validar campos obrigatórios
    newErrors.username = validateField("username", formData.username);
    newErrors.password = validateField("password", formData.password);

    if (!isLogin) {
      newErrors.email = validateField("email", formData.email);
      newErrors.confirmPassword = validateField(
        "confirmPassword",
        formData.confirmPassword
      );
      newErrors.invitationToken = validateField(
        "invitationToken",
        formData.invitationToken
      );
    }

    setErrors(newErrors);

    // Verificar se há erros
    return !Object.values(newErrors).some((error) => error !== "");
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    setIsLoading(true);
    setErrors({});

    try {
      if (isLogin) {
        await loginApi({
          username: formData.username,
          password: formData.password,
        });
      } else {
        await registerApi({
          username: formData.username,
          password: formData.password,
          invitationToken: formData.invitationToken,
        });
        setIsLogin(true);
      }
      navigate("/demo");
    } catch (err: any) {
      setErrors({ general: err.message });
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
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
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
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="bg-gray-900/80 backdrop-blur-xl border border-gray-700/50 rounded-2xl shadow-2xl p-8"
        >
          {/* Tabs */}
          <div className="flex mb-6 bg-gray-800/50 rounded-xl p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`${
                isLogin
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-gray-400 hover:text-gray-200"
              } flex-1 py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-medium`}
            >
              <Shield className="w-4 h-4" /> Entrar
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`${
                !isLogin
                  ? "bg-cyan-600 text-white shadow-lg"
                  : "text-gray-400 hover:text-gray-200"
              } flex-1 py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 font-medium`}
            >
              <User className="w-4 h-4" /> Registrar
            </button>
          </div>

          {/* Error Message */}
          <AnimatePresence>
            {errors.general && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300 text-sm"
              >
                {errors.general}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Form Fields */}
          <div className="space-y-4">
            {/* Username Field */}
            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                Nome de Usuário
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) =>
                    handleInputChange("username", e.target.value)
                  }
                  className={`w-full pl-10 pr-4 py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-all duration-300 ${
                    errors.username
                      ? "border-red-500 focus:ring-red-500/50"
                      : "border-gray-600 focus:ring-cyan-500/50 focus:border-cyan-500"
                  }`}
                  placeholder="Digite seu nome de usuário"
                />
              </div>
              {errors.username && (
                <p className="mt-1 text-red-400 text-xs">{errors.username}</p>
              )}
            </div>

            {/* Email Field (only for register) */}
            <AnimatePresence>
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Email
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) =>
                        handleInputChange("email", e.target.value)
                      }
                      className={`w-full pl-10 pr-4 py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-all duration-300 ${
                        errors.email
                          ? "border-red-500 focus:ring-red-500/50"
                          : "border-gray-600 focus:ring-cyan-500/50 focus:border-cyan-500"
                      }`}
                      placeholder="Digite seu email"
                    />
                  </div>
                  {errors.email && (
                    <p className="mt-1 text-red-400 text-xs">{errors.email}</p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Password Field */}
            <div>
              <label className="block text-gray-300 text-sm font-medium mb-2">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(e) =>
                    handleInputChange("password", e.target.value)
                  }
                  className={`w-full pl-10 pr-12 py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-all duration-300 ${
                    errors.password
                      ? "border-red-500 focus:ring-red-500/50"
                      : "border-gray-600 focus:ring-cyan-500/50 focus:border-cyan-500"
                  }`}
                  placeholder="Digite sua senha"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300 transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-red-400 text-xs">{errors.password}</p>
              )}
            </div>

            {/* Confirm Password Field (only for register) */}
            <AnimatePresence>
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Confirmar Senha
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      value={formData.confirmPassword}
                      onChange={(e) =>
                        handleInputChange("confirmPassword", e.target.value)
                      }
                      className={`w-full pl-10 pr-12 py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-all duration-300 ${
                        errors.confirmPassword
                          ? "border-red-500 focus:ring-red-500/50"
                          : "border-gray-600 focus:ring-cyan-500/50 focus:border-cyan-500"
                      }`}
                      placeholder="Confirme sua senha"
                    />
                    <button
                      type="button"
                      onClick={() =>
                        setShowConfirmPassword(!showConfirmPassword)
                      }
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300 transition-colors"
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="w-4 h-4" />
                      ) : (
                        <Eye className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                  {errors.confirmPassword && (
                    <p className="mt-1 text-red-400 text-xs">
                      {errors.confirmPassword}
                    </p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Invitation Token Field (only for register) */}
            <AnimatePresence>
              {!isLogin && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label className="block text-gray-300 text-sm font-medium mb-2">
                    Token de Convite
                  </label>
                  <div className="relative">
                    <Shield className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="text"
                      value={formData.invitationToken}
                      onChange={(e) =>
                        handleInputChange("invitationToken", e.target.value)
                      }
                      className={`w-full pl-10 pr-4 py-3 bg-gray-800/50 border rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 transition-all duration-300 ${
                        errors.invitationToken
                          ? "border-red-500 focus:ring-red-500/50"
                          : "border-gray-600 focus:ring-cyan-500/50 focus:border-cyan-500"
                      }`}
                      placeholder="Digite o token de convite"
                    />
                  </div>
                  {errors.invitationToken && (
                    <p className="mt-1 text-red-400 text-xs">
                      {errors.invitationToken}
                    </p>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Submit Button */}
          <motion.button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`w-full group relative px-6 py-4 rounded-xl font-semibold text-white transition-all duration-300 transform hover:scale-105 disabled:cursor-not-allowed flex items-center justify-center gap-3 mt-6 ${
              isLoading
                ? "bg-gray-600 animate-pulse"
                : "bg-gradient-to-r from-cyan-600 to-blue-600 shadow-lg hover:shadow-xl"
            }`}
            whileHover={!isLoading ? { y: -2 } : {}}
            whileTap={!isLoading ? { scale: 0.98 } : {}}
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            ) : (
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            )}
            <span>{isLogin ? "Entrar" : "Criar Conta"}</span>
          </motion.button>

          {/* Toggle Mode */}
          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              {isLogin ? "Não tem uma conta?" : "Já tem uma conta?"}{" "}
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-cyan-400 hover:underline"
              >
                {isLogin ? "Registre-se" : "Faça login"}
              </button>
            </p>
          </div>
        </motion.div>

        {/* Footer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-center mt-6 text-gray-500 text-xs"
        >
          <p>© 2025 Shomer - Sistema de Monitoramento Inteligente</p>
        </motion.div>
      </div>
    </div>
  );
}
