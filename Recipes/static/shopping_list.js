'use strict';

const e = React.createElement;
const e = React.createElement;

class ShoppingList extends React.Component {
  render() {
    return (
      <div className="shopping-list">
        <h1>Shopping List for {this.props.name}</h1>
        <ul>
          <li>Instagram</li>
          <li>WhatsApp</li>
          <li>Oculus</li>
        </ul>
      </div>
    );
  }
}

const domContainer = document.querySelector('#shopping_list_container');
ReactDOM.render(e(ShoppingList), domContainer);