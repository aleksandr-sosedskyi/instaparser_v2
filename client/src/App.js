import React from 'react';
import { Provider } from "react-redux";
import store from './store/store';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import {
  HOME
} from './constants/routes';
import Home from "./pages/Home";

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Switch>
          <Route path={HOME} component={Home} />
        </Switch>
      </BrowserRouter>
    </Provider>
  );
}

export default App;
