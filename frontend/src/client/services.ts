import axios from "axios"
import { ApiError } from "./core/ApiError"
import * as sdk from "./generated/sdk.gen"
import type {
  BodyLoginLoginAccessToken,
  ItemCreate,
  ItemUpdate,
  NewPassword,
  UpdatePassword,
  UserCreate,
  UserRegister,
  UserUpdate,
  UserUpdateMe,
} from "./generated/types.gen"

async function data<T>(request: Promise<{ data: T }>): Promise<T> {
  try {
    return (await request).data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new ApiError(
        error.response?.status ?? 0,
        error.response?.data,
        error.message,
      )
    }
    throw error
  }
}

export const UsersService = {
  readUsers: (query: { skip?: number; limit?: number } = {}) =>
    data(sdk.usersReadUsers({ query, throwOnError: true })),
  readUserMe: () => data(sdk.usersReadUserMe({ throwOnError: true })),
  deleteUserMe: () => data(sdk.usersDeleteUserMe({ throwOnError: true })),
  createUser: ({ requestBody }: { requestBody: UserCreate }) =>
    data(sdk.usersCreateUser({ body: requestBody, throwOnError: true })),
  registerUser: ({ requestBody }: { requestBody: UserRegister }) =>
    data(sdk.usersRegisterUser({ body: requestBody, throwOnError: true })),
  updateUserMe: ({ requestBody }: { requestBody: UserUpdateMe }) =>
    data(sdk.usersUpdateUserMe({ body: requestBody, throwOnError: true })),
  updatePasswordMe: ({ requestBody }: { requestBody: UpdatePassword }) =>
    data(sdk.usersUpdatePasswordMe({ body: requestBody, throwOnError: true })),
  updateUser: ({
    userId,
    requestBody,
  }: { userId: string; requestBody: UserUpdate }) =>
    data(
      sdk.usersUpdateUser({
        path: { user_id: userId },
        body: requestBody,
        throwOnError: true,
      }),
    ),
  deleteUser: ({ userId }: { userId: string }) =>
    data(
      sdk.usersDeleteUser({ path: { user_id: userId }, throwOnError: true }),
    ),
}

export const ItemsService = {
  readItems: (query: { skip?: number; limit?: number } = {}) =>
    data(sdk.itemsReadItems({ query, throwOnError: true })),
  createItem: ({ requestBody }: { requestBody: ItemCreate }) =>
    data(sdk.itemsCreateItem({ body: requestBody, throwOnError: true })),
  updateItem: ({ id, requestBody }: { id: string; requestBody: ItemUpdate }) =>
    data(
      sdk.itemsUpdateItem({
        path: { id },
        body: requestBody,
        throwOnError: true,
      }),
    ),
  deleteItem: ({ id }: { id: string }) =>
    data(sdk.itemsDeleteItem({ path: { id }, throwOnError: true })),
}

export const LoginService = {
  loginAccessToken: ({ formData }: { formData: BodyLoginLoginAccessToken }) =>
    data(sdk.loginLoginAccessToken({ body: formData, throwOnError: true })),
  recoverPassword: ({ email }: { email: string }) =>
    data(sdk.loginRecoverPassword({ path: { email }, throwOnError: true })),
  resetPassword: ({ requestBody }: { requestBody: NewPassword }) =>
    data(sdk.loginResetPassword({ body: requestBody, throwOnError: true })),
}
