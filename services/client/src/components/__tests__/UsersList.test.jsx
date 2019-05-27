import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import UsersList from '../UsersList';

const users = [
    {
        'active': true,
        'email': 'nickmostacero@upeu.edu.pe',
        'id': 1,
        'username': 'ldragons'
    },
    {
        'active': true,
        'email': 'pibex.g.m@hotmail.es',
        'id': 2,
        'username': 'brayan'
    }
];

test('UsersList renders properly', () =>{
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children).toBe('ldragons');
});     

test('UsersList renders a snapshot', () =>{
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});  