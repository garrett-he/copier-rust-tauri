import path from "node:path";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vitest/config";

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: [
            { find: "/vite.svg", replacement: path.resolve(__dirname, "tests/__mocks__/fileMock.ts") },
            { find: "/tauri.svg", replacement: path.resolve(__dirname, "tests/__mocks__/fileMock.ts") },
            {
                find: /\.(svg|png|jpg|jpeg|gif|ico)$/,
                replacement: path.resolve(__dirname, "tests/__mocks__/fileMock.ts"),
            },
        ],
    },
    test: {
        globals: true,
        environment: "jsdom",
        coverage: {
            provider: "v8",
            include: ["src/**/*.ts", "src/**/*.vue"],
            exclude: ["src/**/*.d.ts", "src/main.ts"],
            thresholds: {
                branches: 80,
                functions: 80,
                lines: 80,
                statements: 80,
            },
        },
    },
});
