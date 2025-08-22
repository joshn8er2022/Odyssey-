"use client";

import React from "react";

export const SafeLavaLamp: React.FC = () => {
  const [showLamp, setShowLamp] = React.useState(false);
  const [ErrorComponent, setError] = React.useState<null | string>(null);

  React.useEffect(() => {
    // Load after mount to avoid SSR / WebGL startup issues
    const timeout = setTimeout(() => setShowLamp(true), 100);
    return () => clearTimeout(timeout);
  }, []);

  if (ErrorComponent) {
    console.error("LavaLamp failed to load:", ErrorComponent);
    return null;
  }

  if (!showLamp) return null;

  try {
    const { LavaLamp } = require("./fluid-blob");
    return <LavaLamp />;
  } catch (err) {
    setError((err as Error).message);
    return null;
  }
};