import Layout from "@/components/Layout";

export default function ContactsLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return <Layout>{children}</Layout>;
}
