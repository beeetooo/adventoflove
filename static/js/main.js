var HelloMessage = React.createClass({
  render: function() {
  return <div>
  <h1>Hello {this.props.name}</h1>
  <p>Pinchis {this.props.guys}</p>
  </div>
}
});

ReactDOM.render(
<HelloMessage name="John" guys="vatos"/>,
document.getElementById('example')
);
