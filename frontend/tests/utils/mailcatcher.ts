import type { APIRequestContext } from "@playwright/test"

type Email = { id: number | string; recipients: string[]; subject: string }
type MailpitEmail = { ID: string; To: { Address: string }[]; Subject: string }

async function findEmail(
  request: APIRequestContext,
  filter?: (email: Email) => boolean,
) {
  const mailpit = process.env.MAILPIT_HOST
  const url = mailpit
    ? `${mailpit}/api/v1/messages`
    : `${process.env.MAILCATCHER_HOST}/messages`
  const response = await request.get(url)
  if (!response.ok())
    throw new Error(`Mail API failed: HTTP ${response.status()}`)
  const result = await response.json()
  let emails: Email[] = mailpit
    ? result.messages
        .map((mail: MailpitEmail) => ({
          id: mail.ID,
          recipients: mail.To.map((to) => `<${to.Address}>`),
          subject: mail.Subject,
        }))
        .reverse()
    : result
  if (filter) emails = emails.filter(filter)
  return emails.at(-1) ?? null
}

export async function getEmailHtml(
  request: APIRequestContext,
  email: Email,
): Promise<string> {
  const mailpit = process.env.MAILPIT_HOST
  const response = await request.get(
    mailpit
      ? `${mailpit}/api/v1/message/${email.id}`
      : `${process.env.MAILCATCHER_HOST}/messages/${email.id}.html`,
  )
  if (!response.ok())
    throw new Error(`Mail content failed: HTTP ${response.status()}`)
  return mailpit ? (await response.json()).HTML : response.text()
}

export async function findLastEmail({
  request,
  filter,
  timeout = 5000,
}: {
  request: APIRequestContext
  filter?: (email: Email) => boolean
  timeout?: number
}): Promise<Email> {
  const deadline = Date.now() + timeout
  while (Date.now() < deadline) {
    const email = await findEmail(request, filter)
    if (email) return email
    await new Promise((resolve) => setTimeout(resolve, 100))
  }
  throw new Error("Timeout while trying to get latest email")
}
