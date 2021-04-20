import axios from 'axios';
import { BraintreeHostedFields } from 'braintree-web-react';
import $ from "jquery";
import React from 'react';
import Layout from "../../components/Layout";
import braintree from flask;
import Flask, { } from render_template, send_from_directory, request, redirect, jsonify;


class DonateNow extends React.Component {
  constructor() {
      super();
      this.state = {
        clientToken: null,
        instance: null,
      }
  }
  // 
  async componentDidMount() {
    try {
      // Get a client token for authorization from your server
      const response = await axios.get('http://localhost:5000/token')
      const clientToken = response.data

      this.setState({ clientToken })
    } catch (err) {
      console.error(err)
    }
  }

  async buy(e) {
    e.preventDefault();
    try {
      // Setting donor name to localstorage.
      localStorage.setItem("donor", $("#name").val());
      // Send the nonce to your server
      const { nonce } = await this.state.instance.tokenize()

      const response = await axios.post(
        'http://localhost:5000/proc',
        { 
            paymentMethodNonce: nonce ,
            amount: $("#amount").val(),
            name: $("#name").val()
        }
      )
      if(response.data == "OK"){
        location.href = "/Success" 
      }
      else {
        location.href = "/Error"
      }
    } catch (err) { 
      console.error(err)
    }
  }

  render() {
    if (!this.state.clientToken) {
      return (
        <Layout>
          <div className="loading-container">
            <h1>Loading...</h1>
          </div>
          </Layout>
      )
    } else {
      return (
        <Layout>
          <div className="container">
            <BraintreeHostedFields
              className="drop-in-container"
              options={{
                authorization: this.state.clientToken
              }}
              onInstance={(instance) => (this.setState({instance}))}
            >
              <div className="form-container">
                  <form id="cardform">
                      <header>
                          <p className="h3">Help us keep our website running</p>
                          <p>
                              Hi there, thank you for visiting our website. As you know, we provide our content to our visitors free.
                              If you will like to contribute our running costs, you can use this form to donate to us.
                          </p>
                      </header>
                      <div className="row col-12 p-0 m-0 mt-3">
                          <div className="col pl-0">
                              <input type="text" className="form-control" name="name" id="name" placeholder="Name" required />
                          </div>
                          <div className="col pr-0">
                              <input type="number" className="form-control" name="amount" id="amount" placeholder="Amount" required />
                          </div>
                      </div>
                      <div id="card-number" className="input-wrapper mt-4"></div>
                      <div id="expiration-date" className="input-wrapper"></div>
                      <div id="cvv" className="input-wrapper"></div>
                      <div id="postal-code" className="input-wrapper"></div>
                      <input id="button-pay" className="mt-5 m-auto" type="submit" value="Continue" onClick={this.buy.bind(this)} />
                  </form>
              </div>
            </BraintreeHostedFields>
          </div>
        </Layout>
      )
    }
  }
}

export default DonateNow