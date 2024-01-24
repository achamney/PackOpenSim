import React from "react"

class PackList extends React.Component {
    packContainer = React.createRef();
    constructor(props) {
      super(props);
      
      this.state = {
        particles: [],
        hovered: "false",
        selected: "false",
        opening: "false"
      };
      for (let i=0;i<60;i++) {
        this.state.particles.push({})
      }
      this.hovered = false;
    }
    deselectPack = (e) => {
      console.log(e.detail)
      this.setState({selected: "false", opening: "true"});
    }
    selectPack = (e) => {
      e.detail=2;
      this.setState({selected: "true"});
    }
    toggleHover = () => {
      this.setState({hovered: "true"});
    }
    untoggleHover = () => {
      this.setState({hovered: "false"});
    }
    moveMouse = (e) => {
      if (this.state.selected === "true") {
        var dimensions = e.target.getBoundingClientRect();
        this.packContainer.current.style.left = (e.pageX-dimensions.width/2)+"px";
        this.packContainer.current.style.top = (e.pageY-dimensions.height/2)+"px";
        
      }
    }
    render() {
        return (
          <div className="PackContainer" hover={this.state.hovered} ref={this.packContainer}>
            {this.state.particles.map((particle, i)=>{
                return (
                  <div className="particle" id={"particle"+i} key={i}> </div>
                )
              })}
            <div className="Pack" 
              grabbed={this.state.selected} 
              opening={this.state.opening}
              onMouseOver={this.toggleHover} 
              onMouseOut={this.untoggleHover}
              onMouseDown={this.selectPack}
              onMouseUp={this.deselectPack}
              onMouseMove={this.moveMouse}> </div>
          </div>
        );
    }
  }
  
  export default PackList;