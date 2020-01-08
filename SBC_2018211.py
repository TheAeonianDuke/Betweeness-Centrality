#!/usr/bin/env python3
import re
import itertools
from copy import deepcopy
ROLLNUM_REGEX = "201[0-9]{4}"
class  Graph(object):
	name = "Abhishek Pratap Singh"
	email = "abhishek18211@iiitd.ac.in"
	roll_num = "2018211"
	def __init__ (self, vertices, edges):
		self.vertices = vertices		
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))		
		self.edges    = ordered_edges
		mydict={}
		for x in vertices:
			mylist=[]
			for y in edges:
				myfinlist=[]
				if y[0]==x:
					mylist.append(y)        
			mydict[x]=mylist
		#print(mydict)

		def flattendict(dict):
			for x in dict:
				if isinstance(x,list):
					for y in flattendict(x):
						yield y
				else:
					yield x

		mydict = {k: list(flattendict(v)) for k, v in mydict.items()}
		#print(mydict)

		for key, value in mydict.items():
			if key in value:
				value=[x for x in value if x!=key]
				mydict[key]=value
				#print(key,value)
		#print(mydict)

		def invertdict(d):
			inverse={}
			for key in d:
				for item in d[key]:
					if item not in inverse:
						inverse[item]=[key]
					else:
						inverse[item].append(key)
			return inverse

		invertdict=invertdict(mydict)
		#print(invertdict)


		for key in mydict.keys():
			if key not in invertdict.keys():
				invertdict[key]=mydict[key]        
			else:
				invertdict[key].extend(mydict[key])
		#print(invertdict)
		self.finalgraph=invertdict
		self.validate

	def validate(self):
		"""
		Validates if Graph if valid or not

		"""
		if (not isinstance(self.name, str)) or self.name == "":
			raise Exception("Name can't be empty")

		if (not isinstance(self.email, str)) or self.email == "":
			raise Exception("Email can't be empty")

		if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
			raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

		if not all([isinstance(node, int) for node in self.vertices]):
			raise Exception("All vertices should be integers")

		elif len(self.vertices) != len(set(self.vertices)):
			duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])
			raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

		edge_vertices = list(set(itertools.chain(*self.edges)))

		if not all([node in self.vertices for node in edge_vertices]):
			raise Exception("All endpoints of edges must belong in vertices")

		if len(self.edges) != len(set(self.edges)):
			duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])
			raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))


	def all_paths(self,start_node,end_node):
		"""
		Finds all paths from node to destination with length = dist
		"""
		stack = [(start_node, [start_node])]
		#print(len(queue))
		while stack:
			node, path = queue.pop( 0 )
			for next_node in self.finalgraph[node]:
				if next_node in path:
					continue
				elif next_node == end_node:
					yield path + [next_node]
				else:
					stack.append( (next_node, path + [next_node]) )
			

	def get_all_paths(self,start_node,end_node):
		a=list(self.all_paths(start_node,end_node))
		return a   

	def all_shortest_paths(self,start_node,end_node):
		emptylist=[]
		l=self.get_all_paths(start_node,end_node)
		for x in l:
			emptylist.append(len(x))
		#print(emptylist)
		a=min(emptylist)
		b=emptylist.count(a)
		newfinlist=[]
		for x in emptylist:
			if x==a:
				a_index=(emptylist.index(x))
				newfinlist.append(l[a_index])
				emptylist[a_index]=0
				#print(emptylist)
				continue

		#print(newfinlist)
		return newfinlist

	def shortest_path_X(self,start_node,end_node):
		l=self.all_shortest_paths(start_node,end_node)
		return len(l)
	
	def min_dist(self,start_node,end_node):
		"""
		Finds minimum distance between start_node and end_node
		"""
		l=self.all_shortest_paths(start_node,end_node)
		for x in l:
			length=len(x)-1
		return length

	def shortest_path_Y(self,start_node,end_node,node):
		l=self.all_shortest_paths(start_node,end_node)
		l1=deepcopy(l)
		for x in l:
			if node not in x:
				l1.remove(x)
		return len(l1)


	def betweenness_centrality(self,node):
		"""
		Find betweenness centrality of the given node
		"""
		#print(vertices)
		vertices1=deepcopy(vertices)
		if node in vertices1:
			vertices1.remove(node)
		#print(vertices)
		somelist=[]
		
		for x in vertices1:
			for y in range(len(vertices1)):
				somelist.append([vertices1[y], x])	
		
		somelist1=deepcopy(somelist)
		for j in somelist:
			if j[0]>=j[1]:
				somelist1.remove(j)
		#print(somelist1)

		fin_x=[]
		for x in somelist1:
			X,Y=x
			fin_x.append(self.shortest_path_X(X,Y))

		fin_y=[]
		for x in somelist1:
			X,Y=x
			fin_y.append(self.shortest_path_Y(X,Y,node))
		fin_z=[]
		for x in range(len(fin_x)):
			z=fin_y[x]/fin_x[x]
			fin_z.append(z)
		#print(fin_y)
		#print(fin_x)
		#print(fin_z)
		#print((self.vertices))
		btwn_centy=sum(fin_z)
		#print(btwn_centy)
		vertlen=len(vertices)
		stnd_btwn_centy=btwn_centy/(((vertlen-1)*(vertlen-2))/2)
		return stnd_btwn_centy 		

	def top_k_betweenness_centrality(self):
		finalfinal=[]
		for x in vertices:
			centrality=self.betweenness_centrality(x)
			finalfinal.append(centrality)
		#print(vertices)
		#print(finalfinal)
		maxval=max(finalfinal)
		fin=[]
		for i in range(len(vertices)):
			if maxval==finalfinal[i]:
				fin.append(vertices[i])
		return fin

	def __str__(self):
		
		#return list(self.all_paths(start_node,end_node))
		#print (self.get_all_paths(start_node,end_node))
		#print (self.all_shortest_paths(start_node,end_node))
		#print (self.min_dist(start_node,end_node))
		#print (self.betweenness_centrality(1))
		return (self.top_k_betweenness_centrality())

if __name__ == "__main__":
	vertices = [1, 2, 3, 4,5,6,7]
	edges    = [[1,2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 1],[1,7], [2, 7], [3, 7], [4, 7], [5,7], [6,7]]
	graph = Graph(vertices, edges)
	print(graph.__str__())