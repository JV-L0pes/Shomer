// src/components/ExportButton.tsx

import React from "react";
import { motion } from "framer-motion";

export default function ExportButton() {
  return (
    <motion.a
      href="/export_log.csv"
      className="bg-gradient-to-r from-accentLight to-accentDark text-white font-semibold py-3 px-6 rounded-full shadow-2xl hover:shadow-inner transition inline-block"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
    >
      Exportar Registro
    </motion.a>
  );
}
