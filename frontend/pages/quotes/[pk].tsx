import { GetStaticProps, GetStaticPaths } from "next";
import { FC } from "react";
import { QuoteModule } from "@/interfaces";

import Layout from "@/components/Layout";
import ModuleContainer from "@/components/moduledetails/ModuleContainer";
import axios from "axios";

interface QuoteProps {
  quote: QuoteModule;
}

/**
 * A page that renders the HTML of a single quote.
 */
const Quote: FC<QuoteProps> = ({ quote }: QuoteProps) => {
  return (
    <Layout title={""}>
      <ModuleContainer module={quote} />
    </Layout>
  );
};
export default Quote;

export const getStaticProps: GetStaticProps = async ({ params }) => {
  let quote = {};
  const { pk } = params;

  await axios
    .get(`http://django:8000/api/quotes/${pk}/`)
    .then((response) => {
      quote = response.data;
    })
    .catch((error) => {
      // TODO: how should we handle errors here?
    });

  return {
    props: {
      quote,
    },
    revalidate: 10,
  };
};

export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [],
    fallback: "blocking",
  };
};
