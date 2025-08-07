// frontend/src/components/CameraControls.tsx - Controles de Câmera Estilizados
import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Camera, Video, VideoOff, Wifi, Monitor, Loader2 } from "lucide-react";
import { useCameraControl } from "../api";

interface Props {
  className?: string;
}

export default function CameraControls({ className = "" }: Props) {
  const {
    cameraStatus,
    isLoading,
    switchCameraSource,
    toggleStream,
    refreshStatus,
  } = useCameraControl();
  const [switchError, setSwitchError] = useState<string | null>(null);
  const [streamError, setStreamError] = useState<string | null>(null);

  // Atualizar status automaticamente a cada 3 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      refreshStatus();
    }, 3000);

    return () => clearInterval(interval);
  }, [refreshStatus]);

  const handleCameraSwitch = async (source: string) => {
    setSwitchError(null);
    try {
      await switchCameraSource(source);
      // Aguardar um pouco e atualizar status
      setTimeout(() => {
        refreshStatus();
      }, 1000);
    } catch (error) {
      setSwitchError(
        `Erro ao trocar para ${source}: ${
          error instanceof Error ? error.message : "Erro desconhecido"
        }`
      );
    }
  };

  const handleStreamToggle = async () => {
    setStreamError(null);
    try {
      const action = cameraStatus?.stream_enabled ? "stop" : "start";
      await toggleStream(action);
      // Aguardar um pouco e atualizar status
      setTimeout(() => {
        refreshStatus();
      }, 1000);
    } catch (error) {
      setStreamError(
        `Erro ao ${
          cameraStatus?.stream_enabled ? "parar" : "iniciar"
        } stream: ${
          error instanceof Error ? error.message : "Erro desconhecido"
        }`
      );
    }
  };

  const getCurrentCameraIcon = () => {
    return cameraStatus?.current_source === "webcam" ? (
      <Monitor className="w-4 h-4" />
    ) : (
      <Wifi className="w-4 h-4" />
    );
  };

  const getCurrentCameraText = () => {
    return cameraStatus?.current_source === "webcam" ? "Webcam" : "IP Camera";
  };

  const getStreamButtonText = () => {
    if (isLoading) return "Carregando...";
    return cameraStatus?.stream_enabled ? "Parar Stream" : "Iniciar Stream";
  };

  const getStreamButtonIcon = () => {
    if (isLoading) return <Loader2 className="w-4 h-4 animate-spin" />;
    return cameraStatus?.stream_enabled ? (
      <VideoOff className="w-4 h-4" />
    ) : (
      <Video className="w-4 h-4" />
    );
  };

  return (
    <motion.div
      className={`bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="text-lg font-semibold text-cyan-400 mb-4 flex items-center gap-2">
        <Camera className="w-5 h-5" />
        Controles de Câmera
      </h3>

      {/* Status Atual */}
      <div className="mb-6 p-4 bg-gray-700/30 rounded-lg border border-gray-600/30">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {getCurrentCameraIcon()}
            <div>
              <div className="text-sm text-gray-300">Câmera Atual</div>
              <div className="text-lg font-semibold text-white">
                {getCurrentCameraText()}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                cameraStatus?.stream_enabled
                  ? "bg-green-400 animate-pulse"
                  : "bg-red-400"
              }`}
            />
            <span className="text-sm text-gray-300">
              {cameraStatus?.stream_enabled ? "Stream Ativo" : "Stream Inativo"}
            </span>
          </div>
        </div>
      </div>

      {/* Botões de Troca de Câmera */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-300 mb-3">
          Trocar Câmera
        </h4>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => handleCameraSwitch("webcam")}
            disabled={isLoading || cameraStatus?.current_source === "webcam"}
            className={`group relative px-4 py-3 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center gap-2 ${
              cameraStatus?.current_source === "webcam"
                ? "bg-blue-600/50 border border-blue-400/50"
                : "bg-gray-700 hover:bg-gray-600 border border-gray-600 hover:border-gray-500"
            } text-white font-medium`}
          >
            <Monitor className="w-4 h-4" />
            <span>Webcam</span>
            {cameraStatus?.current_source === "webcam" && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-400 rounded-full" />
            )}
          </button>

          <button
            onClick={() => handleCameraSwitch("ip_camera")}
            disabled={isLoading || cameraStatus?.current_source === "ip_camera"}
            className={`group relative px-4 py-3 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center gap-2 ${
              cameraStatus?.current_source === "ip_camera"
                ? "bg-purple-600/50 border border-purple-400/50"
                : "bg-gray-700 hover:bg-gray-600 border border-gray-600 hover:border-gray-500"
            } text-white font-medium`}
          >
            <Wifi className="w-4 h-4" />
            <span>IP Camera</span>
            {cameraStatus?.current_source === "ip_camera" && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-400 rounded-full" />
            )}
          </button>
        </div>
      </div>

      {/* Botão de Controle de Stream */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-300 mb-3">
          Controle de Stream
        </h4>
        <button
          onClick={handleStreamToggle}
          disabled={isLoading}
          className={`w-full group relative px-6 py-4 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed flex items-center justify-center gap-3 ${
            cameraStatus?.stream_enabled
              ? "bg-red-600 hover:bg-red-700 border border-red-500"
              : "bg-green-600 hover:bg-green-700 border border-green-500"
          } text-white font-semibold shadow-lg`}
        >
          {getStreamButtonIcon()}
          <span>{getStreamButtonText()}</span>
        </button>
      </div>

      {/* Informações da IP Camera */}
      {cameraStatus?.current_source === "ip_camera" && (
        <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
          <div className="text-xs text-blue-300 font-medium mb-1">
            IP Camera URL
          </div>
          <div className="text-sm text-blue-200 font-mono break-all">
            {cameraStatus.ip_url}
          </div>
        </div>
      )}

      {/* Mensagens de Erro */}
      {switchError && (
        <motion.div
          className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
        >
          <div className="text-sm text-red-300">{switchError}</div>
        </motion.div>
      )}

      {streamError && (
        <motion.div
          className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
        >
          <div className="text-sm text-red-300">{streamError}</div>
        </motion.div>
      )}

      {/* Dicas de Uso */}
      <div className="mt-4 p-3 bg-gray-700/30 rounded-lg">
        <div className="text-xs text-gray-400">
          <div className="font-medium mb-1">💡 Dicas:</div>
          <ul className="space-y-1 text-xs">
            <li>• Troque de câmera a qualquer momento</li>
            <li>• O stream só é liberado após clicar em "Iniciar Stream"</li>
            <li>• IP Camera deve estar acessível na rede</li>
            <li>• Status atualiza automaticamente a cada 3s</li>
          </ul>
        </div>
      </div>
    </motion.div>
  );
}
