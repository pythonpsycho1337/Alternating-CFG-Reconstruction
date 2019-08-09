/*
 * DSE.java - This file is part of the ACFR
 * Copyright 2019 Johannes Kinder <thpeter@kth.se>
 *
 * This code is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 2 only, as
 * published by the Free Software Foundation.
 *
 * This code is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * version 2 for more details (a copy is included in the LICENSE file that
 * accompanied this code).
 *
 * You should have received a copy of the GNU General Public License version
 * 2 along with this work; if not, see <http://www.gnu.org/licenses/>.
 */
package org.jakstab.util;

import java.util.Set;
import java.util.LinkedList;

import java.io.FileWriter;

import org.jakstab.asm.AbsoluteAddress;
import org.jakstab.cfa.RTLLabel;


/**
 * @author Thomas Peterson
 */
public class DSE {

    public static void exportPaths(Set<LinkedList<RTLLabel>> paths, String filename){//TODO remove intiial pseudo block from paths
        String out = "";

        //Format output
        boolean firstPath = true;
        for (LinkedList<RTLLabel> path : paths) {
            AbsoluteAddress prevAddr = null;

            if (!firstPath) {
                out += "\n";
            }

            boolean firstAddr = true;
            for (RTLLabel statement : path) {
                AbsoluteAddress addr = statement.getAddress();

                if (addr != prevAddr && addr != null){
                    if (!firstAddr){
                        out += ",";
                    }
                    out += addr;
                }

                firstAddr = false;
                prevAddr = addr;
            }

            firstPath = false;

        }

        //Export to file
        try{
            FileWriter fw = new FileWriter(filename);
            fw.write(out);
            fw.close();
        }catch(Exception e){System.out.println(e);}

        System.out.println("exported:");
        System.out.println(out);

    }

}