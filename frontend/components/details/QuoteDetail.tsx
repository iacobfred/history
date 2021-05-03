import { QuoteModule } from "@/interfaces";
import { FC } from "react";
import ImageCard from "../cards/ImageCard";

interface QuoteDetailProps {
  quote: QuoteModule;
}

const QuoteDetail: FC<QuoteDetailProps> = ({ quote }: QuoteDetailProps) => {
  const titleHtml = [quote["attributeeHtml"], quote["dateHtml"]]
    .filter((html) => Boolean(html))
    .join(", ");

  const firstImage = quote["serializedImages"]?.[0];

  return (
    <>
      <h2 className="text-center card-title" dangerouslySetInnerHTML={{ __html: titleHtml }} />

      {firstImage && (
        <div className="img-container" style={{ maxWidth: "44%" }}>
          <ImageCard image={firstImage} />
        </div>
      )}

      <div dangerouslySetInnerHTML={{ __html: quote["html"] }} />

      {quote["tagsHtml"] && (
        <ul className="tags" dangerouslySetInnerHTML={{ __html: quote["tagsHtml"] }} />
      )}

      <footer className="footer sources-footer">
        <ol className="citations">
          {quote["serializedCitations"].map((citation) => (
            <li
              key={citation["pk"]}
              className="source"
              id={`citation-${citation["pk"]}`}
              dangerouslySetInnerHTML={{ __html: citation["html"] }}
            />
          ))}
        </ol>
      </footer>
    </>
  );
};

export default QuoteDetail;
