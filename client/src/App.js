import React from 'react';
import { Provider } from "react-redux";
import store from './store/store';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import {
  HOME
} from './constants/routes';
import Base from "./pages/Base";

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Switch>
          <Route path={HOME} component={Base} />
        </Switch>
      </BrowserRouter>
    </Provider>
  );
}

export default App;
