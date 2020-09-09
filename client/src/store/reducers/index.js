import { combineReducers } from 'redux';
import hackableUsers  from './hackableUsers';
import usersWithSecret from "./usersWithSecret";

export default combineReducers({
    hackableUsers,
    usersWithSecret
});