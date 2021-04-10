import qs from "qs";
import Layout from "../components/Layout";
import axios from "axios";
import {useRouter} from "next/router";
import {useState, useEffect} from "react";

import ModuleCard from "../components/modulecards/ModuleCard";
import ModuleDetail from "../components/moduledetails/ModuleDetail";
import SearchForm from "../components/search/SearchForm";

import {Drawer, Grid} from "@material-ui/core";
import {makeStyles} from "@material-ui/styles";

function useTwoPaneState(...args) {
  const [moduleIndex, setModuleIndex] = useState(...args);
  return [moduleIndex, (e) => {
    if (e.ctrlKey || e.metaKey) return;
    e.preventDefault();
    setModuleIndex(e.currentTarget.dataset.index);
  }];
}

const useStyles = makeStyles({
  drawer: {
    maxWidth: "0px",
    transition: "max-width .15s",
    zIndex: 2,
    "&.open": { maxWidth: "230px" },
  },
  drawerButton: {
    border: "2px solid black",
    zIndex: "10000",
    transition: "transform .15s",
    "&.open": { transform: "translateX(229px)" },
  },
  paper: {
    backgroundColor: "whitesmoke",
    boxShadow: "4px 0 10px -5px #888",
    position: "sticky",
    maxHeight: "100vh",
  },
});

export default function Search({searchResults}) {
  const router = useRouter();
  const [moduleIndex, setModuleIndex] = useTwoPaneState(0);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const classes = useStyles();

  const query = router.query['query'];
  const modules = searchResults['results'] || [];

  const pageHeader = (
    <h1 className='my-0 py-1'>
      {query ?
        <small>{searchResults['count']} results for <b>{query}</b></small>
        :
        <small>{searchResults['count']} items</small>
      }
    </h1>
  );

  if (modules?.length === 0) {
    return (
      <Layout title={"SERCH"}>
        <div className="serp-container">
          <div className="container">
            <p className="lead text-center my-3 py-3">
              There are no results for your search. Please try a different search.
            </p>
            <div className="row">
              {/*<div className="col-12 col-md-6 mx-auto my-3 py-3">*/}
              {/*  <p>{"<Crispy Search Form>"}</p>*/}
              {/*</div>*/}
              <Grid>
                <SearchForm />
              </Grid>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title={"SERCH"}>
      <div className="serp-container">
        <Drawer open={isSearchOpen}
                anchor={"left"}
                variant={"persistent"}
                onClose={() => setIsSearchOpen(false)}
                className={`${classes.drawer} ${isSearchOpen ? "open" : ""}`}
                PaperProps={{className: classes.paper}}>
          <SearchForm/>
        </Drawer>
        <button id="sliderToggle"
                className={`btn ${classes.drawerButton} ${isSearchOpen ? "open" : ""}`}
                onClick={() => setIsSearchOpen(!isSearchOpen)}>
          <i className="fas fa-filter"/>
        </button>

        <div className="display-options">
          {/*{% with selected_option=display_option %}*/}
          {/*<span className="display-option">*/}
          {/*                      <input type="radio" id="2pane-option" name="display" value="2pane"*/}
          {/*                             {% if selected_option == '2pane' or not selected_option %} checked{% endif %} />*/}
          {/*                      <label htmlFor="2pane-option"><i className="fas fa-list"></i></label>*/}
          {/*                  </span>*/}
          {/*<span className="display-option">*/}
          {/*                      <input type="radio" id="rows-option" name="display" value="rows"*/}
          {/*                             {% if selected_option == 'rows' %} checked{% endif %} />*/}
          {/*                      <label htmlFor="rows-option"><i className="fas fa-bars"></i></label>*/}
          {/*                  </span>*/}
          {/*<span className="display-option">*/}
          {/*                      <input type="radio" id="timeline-option" name="display" value="timeline"*/}
          {/*                             {% if selected_option == 'timeline' %} checked{% endif %} />*/}
          {/*                      <label htmlFor="timeline-option"><i className="fas fa-columns"></i></label>*/}
          {/*                  </span>*/}
          {/*{% endwith %}*/}
        </div>

        <div className="results-container">
          {pageHeader}
          {/*{% if display_option == '2pane' or not display_option %}*/}
          <div className="two-pane-container">
            <div className="results result-cards">
              {modules.map((module, index) => (
                <a href={module['absolute_url']} className="result 2pane-result"
                   data-href={module['absolute_url']} data-key={module['slug']}
                   key={module['absolute_url']} data-index={index}
                   onClick={setModuleIndex}
                >
                  <ModuleCard module={module}/>
                </a>
              ))}
            </div>
            <div className="card view-detail sticky">
              <ModuleDetail module={modules[moduleIndex]}/>
            </div>
          </div>
          {/*{% elif display_option == 'rows' %}*/}
          {/*<div className="container results">*/}
          {/*  {% for object in object_list %}*/}
          {/*  <div className="result" data-key="{{ object.slug }}">*/}
          {/*    {{object | get_detail_html}}*/}
          {/*  </div>*/}
          {/*  <hr style="clear: both"/>*/}
          {/*  {% endfor %}*/}
          {/*</div>*/}
          {/*{% elif display_option == 'timeline' %}*/}
          {/*<p>Not yet implemented</p>*/}
          {/*{% endif %}*/}
        </div>
      </div>
    </Layout>
  );
}

export async function getServerSideProps(context) {
  let searchResults = {};

  await axios
    .get("http://django:8000/api/search/", {
      params: context.query,
      paramsSerializer: (params) => (
        qs.stringify(params, {arrayFormat: "repeat"})
      ),
    })
    .then((response) => {
      searchResults = response.data;
    })
    .catch((error) => {
      // console.error(error);
    });

  return {
    props: {
      searchResults,
    },
  };
}