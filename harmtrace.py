from typing import List
import subprocess
import argparse
import re
import nltk
import jams

SYNTAX_TREE_RE = re.compile(r"(?<=\n)(\[(.*)\])")
CLEAN_TREE_RE = re.compile(r"_\w+")

def read_jams(path: str):
  jam = jams.load(path, validate=False)
  namespaces = [ str(a.namespace) for a in jam.annotations ]
  key = jam.search(namespace="key_mode")[0].data[0].value
  chord_namespace = "chord_harte" if "chord_harte" in namespaces else "chord"
  chords = " ".join([f"{obs.value};{obs.duration}" for obs in jam.search(namespace=chord_namespace)[0].data])
  return f"{key} {chords}"
        

def run_command(chords: List[str], grammar: str = "jazz"):
  command = f"docker exec harmtracepy stack exec harmtrace parse -- --grammar={grammar} --chords=\"{chords}\""
  docker_output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL).decode("utf8")
  syntax_tree = SYNTAX_TREE_RE.search(docker_output).groups()[0]
  return syntax_tree

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Harmtrace python wrapper")
  parser.add_argument("--grammar", choices=["pop", "jazz"], default="jazz")
  parser.add_argument("--show", default=False, action="store_true")
  parser.add_argument("--pretty", default=False, action="store_true")
  parser.add_argument("--out", default=None, type=str)

  input_group = parser.add_mutually_exclusive_group(required=True)
  input_group.add_argument("--chords")
  input_group.add_argument("--jams")

  args = parser.parse_args()
  
  if args.chords is not None:
    chords = args.chords
  elif args.jams is not None:
    chords = read_jams(args.jams)
 
  harmtrace_tree = run_command(chords, grammar=args.grammar)
  print(harmtrace_tree)

  tree = nltk.tree.Tree.fromstring(harmtrace_tree, brackets="[]")
  drawer = nltk.draw.tree.TreeView(tree)
  
  if args.pretty:
    print(tree.pretty_print())
  if args.show:
    drawer.mainloop()
  if args.out is not None:
    drawer._cframe.print_to_file(args.out)

