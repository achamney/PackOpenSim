import React from "react"
import Pack from "./Pack.js"
var packs = [{key:1}];

class PackList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
          value: null,
        };
      }
    render() {
        return (
        <div className="PackList">
            {packs.map(pack=>{
                return (
                    <Pack key={pack.key} />
                )
            })}
        </div>
        );
    }
  }
  
  export default PackList;