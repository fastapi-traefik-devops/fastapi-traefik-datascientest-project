import type { UserPublic } from "../../src/client"

// This endpoint exists exclusively for ENVIRONMENT=local.
export const createUser = async ({
  email,
  password,
}: { email: string; password: string }): Promise<UserPublic> => {
  const response = await fetch(
    `${process.env.VITE_API_URL}/api/v1/private/users/`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, full_name: "Test User" }),
    },
  )
  if (!response.ok)
    throw new Error(`Test user creation failed: HTTP ${response.status}`)
  return response.json()
}
