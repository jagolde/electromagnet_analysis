import grama as gr
import numpy as np
import matplotlib.pyplot as plt
DF = gr.Intention()

free_space_permeability = 4*np.pi*10**-7
relativity_permeability_of_air = 1.0000037
effective_permeability = relativity_permeability_of_air/free_space_permeability

var_electro = ["winds","current","eff_core_length","core_width","magnet_dist","overlapping_area"]
out_electro = ["magnetic_field"]

def electromatnetic_force(df):

    magnetic_field = (effective_permeability*df.winds*df.current)/2 * ...
    (np.cos(np.tan(df.core_width/(df.eff_core_length+df.magnet_dist))) - np.cos(np.tan(df.core_width/df.magnet_dist)))

    #magnetic_force = (magnetic_field**2 * overlapping_area)/(2*free_space_permeability)

    return gr.df_make(force=magnetic_field)


md_electro =(
    gr.Model()
    >> gr.cp_vec_function(
        fun=electromatnetic_force,
        var=var_electro,
        out=out_electro
    )
    >> gr.cp_bounds(
        winds=(),
        current=(),
        eff_core_length=(),
        core_width=(),
        magnet_dist=(),
        overlapping_area=()
    )
)

df_res = (
    md_electro
    >> gr.ev_min(
        out_min=out_electro,
        n_restarts=10
    )
)

md_electro.printpretty()