import axiosWithoutAuth from "@/axiosWithoutAuth";
import ModuleContainer from "@/components/details/ModuleContainer";
import ModuleDetail from "@/components/details/ModuleDetail";
import Layout from "@/components/Layout";
import { ImageModule } from "@/interfaces";
import { GetStaticPaths, GetStaticProps } from "next";
import { FC } from "react";

interface ImageProps {
  image: ImageModule;
}

/**
 * A page that renders the HTML of a single image.
 */
const Image: FC<ImageProps> = ({ image }: ImageProps) => {
  return (
    <Layout title={image["name"]}>
      <ModuleContainer>
        <ModuleDetail module={image} />
      </ModuleContainer>
    </Layout>
  );
};
export default Image;

export const getStaticProps: GetStaticProps = async ({ params }) => {
  let image = {};
  const { slug } = params;
  const body = {
    query: `{
      image(slug: "${slug}") {
        name
        slug
        description
        serializedImages
        model
        adminUrl
      }
    }`,
  };
  await axiosWithoutAuth
    .post("http://django:8000/graphql/", body)
    .then((response) => {
      image = response.data.data.image;
    })
    .catch((error) => {
      // console.error(error);
    });

  return {
    props: {
      image,
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
