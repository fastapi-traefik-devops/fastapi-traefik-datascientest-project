import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "./openapi.json",
  output: "./src/client/generated",
  plugins: [
    "@hey-api/typescript",
    "@hey-api/client-axios",
    { name: "@hey-api/sdk", operations: { strategy: "flat" } },
  ],
})
