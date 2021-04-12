import OccurrenceDetail from "./OccurrenceDetail";
import QuoteDetail from "./QuoteDetail";
import { createRef, useLayoutEffect } from "react";

export default function ModuleDetail({ module }) {
  const ref = createRef();
  useLayoutEffect(() => {
    // After the DOM has rendered, check for lazy images
    // and set their `src` to the correct value.
    // This is not an optimal solution, and will likely change
    // after redesigning how backend HTML is served.
    const images = ref.current.getElementsByTagName("img");
    for (const img of images) {
      if (img.dataset["src"]) img.src = img.dataset["src"];
    }
    // force switching between modules to scroll
    // to the top of the new module
    ref.current.parentElement.scrollTop = 0;
  }, [module]);

  let details;
  switch (module["model"]) {
    // TODO: add more models here as soon as they
    //       may appear on the SERP.
    case "occurrences.occurrence":
      details = <OccurrenceDetail occurrence={module} />;
      break;
    case "quotes.quote":
      details = <QuoteDetail quote={module} />;
      break;
    default:
      details = <pre>{JSON.stringify(module)}</pre>;
  }

  // TODO: conditionally render edit button for super users
  //       with NextAuth's `useSession()`.
  // const superUserEditButton = (
  //   <a href="{% url 'admin:occurrences_occurrence_change' occurrence.pk %}"
  //      target="_blank" className="edit-object-button" rel="noopener noreferrer"
  //      style={{display: "inline-block", position: "absolute", top: "1px", right: "-2rem", fontWeight: "bold"}}>
  //     <i className="fa fa-edit"/>
  //   </a>
  // );

  return (
    <div className="detail" ref={ref}>
      {details}
    </div>
  );
}